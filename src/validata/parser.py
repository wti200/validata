"""Module containing the Parser class for complex boolean expressions."""

import logging
import numpy as np

from validata.tokenizer import Tokenizer
from validata.evaluator import Evaluator


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

    # Define the tokens
    token_types = {
        "AND": [" and ", " & "],
        "OR": [" or ", " | "],
        "GROUP_OPEN": "(",
        "GROUP_CLOSE": ")",
    }

    def __init__(self, expression, name="validation_result"):
        self._log = logging.getLogger(__name__)

        # Replace new lines for multi-line expressions
        expression = expression.replace("\n", " ")
        self._tokenizer = Tokenizer(expression, self.token_types)
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
                    self._log.debug("Processing token: %s", next_token.value)
                    self._log.debug("Evaluating right hand side expression.")
                    right_hand = Evaluator(next_token.value).evaluate(df)

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
                self._log.debug("Evaluating expression: %s", token.value)

                if result is not None:
                    raise ValueError("Expected and / or, got expression instead.")

                result = Evaluator(token.value).evaluate(df)

        result.columns = [self._name]
        return result
