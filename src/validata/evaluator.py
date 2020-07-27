"""Module containing the Evaluator class for evaluating simple boolean expressions."""

import re
import logging

from validata.operators import Operator, DataOperator, LogicalOperator
from validata.comparators import Comparator


class Evaluator:
    """Evaluator class for parsing and evaluating simple boolean expressions."""

    def __init__(self, expression):
        self._log = logging.getLogger(__name__)
        self._expression = expression

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
            cols = {col for col in columns if col.startswith(col_expr[:-1])}
            if not cols:
                raise RuntimeError(
                    f"No columns were selected using expression: {col_expr}."
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

    @staticmethod
    def _parse_expression(expression):
        """Parse expression into its component parts."""

        # Define regexes for component parts
        op_expr = "|".join([re.escape(op) for op in Operator.list()])
        comp_expr = "|".join([re.escape(comp) for comp in Comparator.list()])
        col_expr = r"(:?[a-z0-9\_\*]+(?:\s+\+\s+)?)+"

        # Compile into a single expression pattern
        pattern = (
            r"(?:(?P<op>^{op})\s+)?"  # Optional Operator + space
            + r"(?P<cols>{col})\s+"  # Required column pattern + space
            + r"(?P<comp>{comp})"  # Required Comparator
            + r"(?:(?:\s+(?P<value>.*))|$)"  # Optional space + value or end
        )
        pattern = re.compile(
            pattern.format(op=op_expr, col=col_expr, comp=comp_expr), re.IGNORECASE
        )

        # Match to the provided expression
        match = re.match(pattern, expression)
        if not match:
            raise ValueError(f"Invalid expression: {expression}.")

        op = match.group("op")
        op = op.strip().lower() if op else None
        cols = match.group("cols")
        comp = match.group("comp").lower()
        value = match.group("value")

        return op, cols, comp, value

    def evaluate(self, df):
        """Evaluate the expression against the provided data frame."""

        # Get components from the expression
        op, cols, comp, value = self._parse_expression(self._expression)

        cols = self._select_columns(cols, df.columns)
        self._log.debug("Selected columns: %s.", ", ".join(cols))

        comp = Comparator.get(comp)
        self._log.debug("Using comparator: %s.", comp.__class__.__name__)

        if op:
            op = Operator.get(op)
            self._log.debug("Using operator: %s.", op.__class__.__name__)

        # Perform comparison and operation
        if op:
            if isinstance(op, LogicalOperator):
                result = df[cols].pipe(comp, target=value).pipe(op)
            elif isinstance(op, DataOperator):
                result = df[cols].pipe(op).pipe(comp, target=value)
            else:
                raise TypeError(f"Unknown operator type: {op.__class__.__name__}.")

        else:
            if len(cols) > 1:
                raise RuntimeError(
                    f"Too many columns ({len(cols)}) to compare, either select "
                    "a single column or reduce columns using an operator."
                )

            result = df[cols].pipe(comp, target=value)

        return result
