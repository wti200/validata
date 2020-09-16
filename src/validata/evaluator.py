"""Module containing the Evaluator class for evaluating simple boolean expressions."""

import logging

from validata.operators import Operator, DataOperator, LogicalOperator
from validata.comparators import Comparator


class Evaluator:
    """
    Evaluator class for parsing and evaluating simple boolean expressions.

    Parameters
    ----------
    columns : List[str]
        List of column names or regular expression used to select columns.
    comparator : str
        Identifier for a Comparator class.
    value : str
        Value to compare against.
    operator : str
        Identifier for an Operator class.
    """

    def __init__(self, columns, comparator, value, operator=None):
        self._log = logging.getLogger(__name__)
        self._columns = columns
        self._comparator = comparator
        self._value = value
        self._operator = operator

    def evaluate(self, df):
        """
        Evaluate the expression against the provided data frame.

        Parameters
        ----------
        df : pandas.DataFrame
            Data set to evaluate the expression against.

        Returns
        -------
        pandas.DataFrame
            Single-column DataFrame with validation results.
        """

        self._log.debug("Selected columns: %s.", ", ".join(self._columns))

        comp = Comparator.get(self._comparator)
        self._log.debug("Using comparator: %s.", comp.__class__.__name__)

        if op:
            op = Operator.get(self._operator)
            self._log.debug("Using operator: %s.", op.__class__.__name__)

        # Perform comparison and operation
        if op:
            if isinstance(op, LogicalOperator):
                result = df[self._columns].pipe(comp, target=self._value).pipe(op)
            elif isinstance(op, DataOperator):
                result = df[self._columns].pipe(op).pipe(comp, target=self._value)
            else:
                raise TypeError(f"Unknown operator type: {op.__class__.__name__}.")

        else:
            if len(self._columns) > 1:
                raise RuntimeError(
                    f"Too many columns ({len(self._columns)}) to compare, either select "
                    "a single column or reduce columns using an operator."
                )

            result = df[self._columns].pipe(comp, target=self._value)

        return result
