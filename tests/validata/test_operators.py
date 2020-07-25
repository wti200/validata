"""Module for unit testing Operator classes."""

import pytest
import pandas as pd

from validata.operators import Operator

OPERATORS = Operator.list()


class TestOperators:
    """Class providing unit tests for Operator classes."""

    @staticmethod
    def _apply_operator(operator, df):
        """Applies an Operator to a DataFrame."""

        operator = Operator.get(operator)
        return operator(df)

    @pytest.mark.parametrize("operator", OPERATORS)
    def test_returns_frame(self, operator, dummy_data):
        """Test whether operator returns a pandas DataFrame."""

        result = self._apply_operator(operator, dummy_data)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.parametrize("operator", OPERATORS)
    def test_returns_frame_on_single_column(self, operator, dummy_data):
        """
        Test whether operator returns a pandas DataFrame even if only a
        single column is provided as input.
        """

        result = self._apply_operator(operator, dummy_data)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.parametrize("operator", OPERATORS)
    def test_shape(self, operator, dummy_data):
        """Test whether operator returns DataFrame with shape nrow, 1."""

        nrow = dummy_data.shape[0]
        result = self._apply_operator(operator, dummy_data)
        assert result.shape == (nrow, 1)
