"""Module containing the Validator class for performing data validation."""

import logging
import pandas as pd

from .operators import Operators
from .comparators import Comparators


class Validator:
    """
    Data validator class, takes a DataFrame of validation checks and
    runs them against a dataset.

    Parameters
    ==========
    df_checks : pandas.DataFrame
        DataFrame containing validation check definitions. Each check should
        provide the following fields:

        - check_id:   Name of the validation check.
        - columns:    Expression (string) to apply validation to.
        - oparation:  Operation to perform (optional, see operators.py)
        - comparison: Comparison to perform (required, see comparators.py)
        - value:      Target value to compare to.
    """

    # Required columns in validation checks
    _required = ["check_id", "columns", "operation", "comparison", "value"]

    def __init__(self, df_checks):
        # Check and store validation checks
        self._check_validations(df_checks)
        self._checks = df_checks[self._required]

        # Set  up logger
        self._log = logging.getLogger(__name__)

    def _check_validations(self, df_checks):
        """
        Checks whether validations are correctly specified.

        Parameters
        ==========
        df_checks : pandas.DataFrame
            DataFrame containing validation check definitions.
        """

        if not isinstance(df_checks, pd.DataFrame):
            raise TypeError("Please supply validation definitions as pandas DataFrame.")

        missing = set(self._required) - set(df_checks.columns)
        if missing:
            raise RuntimeError(
                f"Missing columns from validation definitions: {', '.join(missing)}."
            )

        operations = set(self._checks["operation"].dropna())
        missing = operations - Operators.list()
        if missing:
            raise RuntimeError(
                f"Unknown operations in validation definitions: {', '.join(missing)}."
            )

        comparisons = set(self._checks["comparison"].dropna())
        missing = comparisons - Comparators.list()
        if missing:
            raise RuntimeError(
                f"Unknown comparison in validation definitions: {', '.join(missing)}."
            )

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

    def validate(self, df):
        """
        Validates a pandas DataFrame against the checks provided to the
        Validator class.

        Parameters
        ==========
        df : pandas.DataFrame
            DataFrame containing the data to be validated.

        Returns
        =======
        pandas.DataFrame
            DataFrame with one column for each validation check.
        """

        # Looping through the validation checks
        results = pd.DataFrame(index=df.index)
        for cid, col_expr, op, cmp, target in self._checks.to_records(index=False):
            self._log.debug("Performing validation: %s...", cid)

            # Must define a comparison
            if not cmp:
                raise RuntimeError(f"No comparison defined for check {cid}.")

            # Select relevant columns from the data
            cols = self._select_columns(col_expr, df.columns)
            self._log.debug("Selected columns: %s", ", ".join(cols))

            # Fetch comparator and (optionally) operator
            cmp = Comparators.get(cmp)
            self._log.debug("Using comparator: %s", cmp.__class__.__name__)
            if op:
                op = Operators.get(op)
                self._log.debug("Using operator: %s", op.__class__.__name__)

            # Perform comparison and operation
            if op:
                if op.apply == "after":
                    result = df[cols].pipe(cmp, target=target).pipe(op)
                else:
                    result = df[cols].pipe(op).pipe(cmp, target=target)
            else:
                if len(cols) > 1:
                    raise RuntimeError(
                        f"Validation {cid}: Too many columns ({len(cols)}) to compare, "
                        "either select a single column or combine columns with an operator."
                    )

                result = df[cols].pipe(cmp, target=target)

            results[cid] = result
            self._log.debug(
                "Validated %d rows - %0.0f evaluated to True.",
                len(result),
                100 * result.sum()[0] / len(result),
            )
            self._log.debug("Finished validation: %s...", id)

        return results
