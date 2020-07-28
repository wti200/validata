"""Module containing the Validator class for performing data validation."""

import logging
import pandas as pd

from validata.parser import Parser


class Validator:
    """
    Data validator class, takes a DataFrame of validation checks and
    runs them against a dataset.

    Parameters
    ----------
    df_checks : pandas.DataFrame
        DataFrame containing validation definitions. Each validation should
        provide the following information:

        - name:         Name of the validation check.
        - expression:   Boolean expression for the validation check.
    """

    # Required columns in validation checks
    _required = ["name", "expression"]
    _results = None

    def __init__(self, df_checks):
        self._log = logging.getLogger(__name__)

        # Check and store validation checks
        self._check_validations(df_checks)
        self._checks = df_checks[self._required]

    def _check_validations(self, df_checks):
        """
        Checks whether validations are correctly specified.

        Parameters
        ----------
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
        ----------
        df : pandas.DataFrame
            DataFrame containing the data to be validated.

        Returns
        -------
        pandas.DataFrame
            DataFrame with one column for each validation check.
        """

        # Looping over the validation checks
        results = pd.DataFrame(index=df.index)
        for name, expression in self._checks.to_records(index=False):
            self._log.debug("Performing validation: %s.", name)

            parser = Parser(expression)
            result = parser.evaluate(df)

            results[name] = result

            self._log.debug(
                "Validated %d rows - %0.0f%% evaluated to True.",
                len(result),
                100 * result.sum()[0] / len(result),
            )
            self._log.debug("Finished validation: %s.", name)

        self._results = results
        return results

    def get_summary(self, per="validation", percentage=True):
        """
        Get a summary of the last validation run.

        Parameters
        ----------
        per : Optional[str]
            String indicating whether to summarize per validation (default)
            or per case.
        pecentage : Optional[bool]
            Report percentages (True, default) or counts (False).

        Returns
        -------
        pandas.DataFrame
            Data frame with summary statistics per validation or case.
        """

        if self._results is None:
            raise RuntimeError("No validation has run yet, call validate() first.")

        axis = 1 if per == "case" else 0
        summary = self._results.sum(axis=axis)

        name = "positive"
        if percentage:
            summary = 100 * summary / self._results.shape[axis]
            name = "percentage_positive"

        return summary.to_frame(name)
