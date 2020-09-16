"""Module containing the Parser class for complex boolean expressions."""

import logging
import numpy as np

from validata.tokenizer import Tokenizer
from validata.evaluator import Evaluator
from validata.operators import Operator
from validata.comparators import Comparator


class Parser:
    """
    Parses for complex, nested boolean expressions.

    Parameters
    ----------
    expression : str
        Logical expression as string, some examples:
        - column_1 >= 30000
        - column_1 >= 2 and (column_2 missing or column_2 missing)
        - column_1 == 1 and any dummy_* == 1
    name : Optional[str]
        Name for the validation, defaults to "validation_result".
    """

    def __init__(self, expression, name="validation_result"):
        self._log = logging.getLogger(__name__)

        # TO DO: Check for duplicate names
        token_types = {op: "OPERATOR" for op in Operator.list()}
        token_types.update({comp: "COMPARATOR" for comp in Comparator.list()})
        self._tokenizer = Tokenizer(expression, token_types)

        self._name = name

    def evaluate(self, df):
        """
        Evaluate the logical expression against the provided pandas DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Data set to evaluate the expression against.

        Returns
        -------
        pandas.DataFrame
            Single-column DataFrame with validation results.
        """

        result = None

        for token in self._tokenizer:

            self._log.debug("Processing token: %s [%s]", token.value, token.type)

            # Handle grouping / nesting
            if token.type == "GROUP_OPEN":
                self._log.debug("Entering nested expression.")
                result = self.evaluate(df)

            elif token.type == "GROUP_CLOSE":
                self._log.debug("Exiting nested expression.")
                break

            elif token.type in ["AND", "OR"]:
                self._log.debug("Processing %s expression.", token.value)

                if result is None:
                    raise ValueError(
                        "Use of and / or without left hand side expression."
                    )

                # Get right hand side, compute results
                next_token = next(self._tokenizer)
                if next_token.type == "GROUP_OPEN":
                    self._log.debug(
                        "Processing token: %s [%s]", next_token.value, next_token.type
                    )
                    self._log.debug("Entering nested right hand side expression.")
                    right_hand = self.evaluate(df)

                else:
                    self._log.debug("Evaluating right-hand expression.")

                    # Collect all tokens related to the expression
                    expression = [next_token]
                    for tkn in self._tokenizer:
                        expression.append(tkn)
                        next_token = self._tokenizer.peek()
                        if next_token and next_token.type in [
                                "AND",
                                "OR",
                                "GROUP_OPEN",
                                "GROUP_CLOSE",
                        ]:
                            break

                    # Classify parts and evaluate the expression
                    op, cols, comp, val = self._classify_parts(expression)
                    cols = self._select_columns(df, cols)
                    self._log.debug(
                        "Operator: %s, Columns: %s, Comparator: %s, Value: %s",
                        op,
                        [col.value for col in cols],
                        comp,
                        val,
                    )
                    right_hand = Evaluator(cols, comp, val, op).evaluate(df)

                # Apply and / or operation
                if token.type == "AND":
                    # result = result and right_hand
                    result = np.all(
                        result.join(right_hand, rsuffix="_rh"), axis=1
                    ).to_frame()

                else:
                    # result = result or right_hand
                    result = np.any(
                        result.join(right_hand, rsuffix="_rh"), axis=1
                    ).to_frame()

            else:
                self._log.debug("Evaluating logical expression.")

                if result is not None:
                    raise ValueError("Expected and / or, got expression instead.")

                # Collect all tokens related to the expression
                expression = [token]
                for tkn in self._tokenizer:
                    expression.append(tkn)
                    next_token = self._tokenizer.peek()
                    if next_token and next_token.type in [
                            "AND",
                            "OR",
                            "GROUP_OPEN",
                            "GROUP_CLOSE",
                    ]:
                        break

                # Classify parts and evaluate the expression
                op, cols, comp, val = self._classify_parts(expression)
                cols = self._select_columns(df, cols)
                self._log.debug(
                    "Operator: %s, Columns: %s, Comparator: %s, Value: %s",
                    op,
                    cols,
                    comp,
                    val,
                )
                result = Evaluator(cols, comp, val, op).evaluate(df)

        result.columns = [self._name]
        return result

    @staticmethod
    def _classify_parts(token_list):
        """
        Classify different parts of the provided token list.

        Parameters
        ----------
        token_list : List[validata.tokenizer.Token]
            List of tokens from the Tokenizer class.

        Returns
        -------
        Tuple[str, list, str, str]
            Tuple of operator, columns, comparator, and target value.
        """

        operator = None
        comparator = None
        columns = []
        value = []

        for token in token_list:
            if token.type == "OPERATOR":
                operator = token.value
            elif token.type == "COMPARATOR":
                comparator = token.value
            elif not comparator:
                if token.value == "+":
                    continue
                columns.append(token)
            else:
                value.append(token.value)

        return operator, columns, comparator, " ".join(value)

    @staticmethod
    def _select_columns(df, column_tokens):
        """
        Select columns from a DataFrame based on al list of column tokens.
        """

        selected = []
        for token in column_tokens:

            # Match by regular expression
            if token.type == "REGEX":
                cols = df.columns[df.columns.str.contains(token.value, regex=True)]
                selected.extend(cols)

            # Match by name
            else:
                col_name = token.value
                if col_name.endswith("*"):
                    cols = {col for col in df.columns if col.startswith(col_name[:-1])}
                    if not cols:
                        raise RuntimeError(
                            f"No columns were selected using expression: '{col_name}'."
                        )
                    selected.extend(cols)

                else:
                    if col_name not in df.columns:
                        raise RuntimeError(
                            f"Column '{col_name}' not found in the data."
                        )
                    selected.append(col_name)

        return set(selected)
