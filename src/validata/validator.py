"""Module containing the Validator class for performing data validation."""

import logging
import pandas as pd

from validata.boolean_parser import BooleanParser


class Validator:
    """
    Data validator class, takes a DataFrame of validation checks and
    runs them against a dataset.

    Parameters
    ==========
    df_checks : pandas.DataFrame
        DataFrame containing validation check definitions. Each check should
        provide the following fields:

        - name:         Name of the validation check.
        - expression:   Boolean expression for the validation check.
    """

    # Required columns in validation checks
    _required = ["name", "expression"]

    def __init__(self, df_checks):
        self._log = logging.getLogger(__name__)

        # Check and store validation checks
        self._check_validations(df_checks)
        self._checks = df_checks[self._required]

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

        # Looping over the validation checks
        results = pd.DataFrame(index=df.index)
        for name, expression in self._checks.to_records(index=False):
            self._log.debug("Performing validation: %s.", name)

            parser = BooleanParser(expression)
            result = parser.evaluate(df)

            results[name] = result

            self._log.debug(
                "Validated %d rows - %0.0f%% evaluated to True.",
                len(result),
                100 * result.sum()[0] / len(result),
            )
            self._log.debug("Finished validation: %s.", name)

        return results
