"""Module containing the Evaluator class for evaluating simple boolean expressions."""

import logging

from data_validation.tokenizer import Tokenizer
from data_validation.operators import Operators
from data_validation.comparators import Comparators

class Evaluator:
    """Evaluator class for parsing and evaluating simple boolean expressions."""

    def __init__(self, expression):
        self._log = logging.getLogger(__name__)

        # Construct token types
        self._expression = expression
        token_types = {
            "COMPARATOR": Comparators.list(),
            "OPERATOR": Operators.list(),
        }
        self._tokenizer = Tokenizer(expression, token_types)

    @staticmethod
    def _select_columns(col_expr, columns):
        """
        Selects columns based on provided column expressions:

        - Multiple columns can be provided using + signs
        - Wildcard * can be used to allow pattern matching
        - If no special characters are found, a single column is assumed.

        Parameters
        ==========
        col_expr : str
            Expression for selecting one or more columns.
        columns : pandas.Index
            Columns from the DataFrame being validated.

        Returns
        =======
        set
            Set of selected column names
        """

        if "*" in col_expr:
            cols = {col.startswith(col_expr.strip("*")) for col in columns}
            if not cols:
                raise RuntimeError(
                    f"No columns were selected using expression {col_expr}."
                )

        else:
            cols = {col.strip() for col in col_expr.split("+")}
            missing = cols - set(columns)
            if missing:
                raise RuntimeError(
                    f"Columns from expression '{col_expr}' are missing in the data: "
                    + ", ".join(missing)
                )

        return cols

    def evaluate(self, df):
        """Evaluate the expression against the provided data frame."""

        tokens = [token for token in self._tokenizer]
        types = [tokens.type for token in tokens]

        # Expecting pattern: (OPERATOR) COLUMNS COMPARATOR VALUE
        if types == ["OPERATOR", "BARE WORD", "COMPARATOR", "BARE WORD"]:
            op, cols, comp, value = [t.value for t in tokens]
        elif types == ["BARE WORD", "COMPARATOR", "BARE WORD"]:
            op = None
            cols, comp, value = [t.value for t in tokens]
        else:
            raise ValueError(f"Invalid expression: {self._expression}.")

        comp = Comparators.get(comp)
        cols = self._select_columns(cols, df.columns)
        self._log.debug("Selected columns: %s", ", ".join(cols))

        self._log.debug("Using comparator: %s", comp.__class__.__name__)
        if op:
            op = Operators.get(op)
            self._log.debug("Using operator: %s", op.__class__.__name__)

        # Perform comparison and operation
        if op:
            if op.apply == "after":
                result = df[cols].pipe(comp, target=value).pipe(op)
            else:
                result = df[cols].pipe(op).pipe(comp, target=value)
        else:
            if len(cols) > 1:
                raise RuntimeError(
                    f"Too many columns ({len(cols)}) to compare, "
                    "either select a single column or combine columns with an operator."
                )

            result = df[cols].pipe(comp, target=value)

        return result
