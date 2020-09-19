"""Module for test base classes."""

import numpy as np
import pandas as pd

from validata.operators import Operator
from validata.comparators import Comparator


class BaseOperatorTests:
    """Class providing basic unit tests for Operator classes."""

    operator = NotImplemented
    data = pd.DataFrame()
    expected = NotImplemented

    def _apply(self, df):
        """Applies a Operator to a DataFrame."""

        operator = Operator.get(self.operator)
        return operator(df)

    def test_returns_frame(self):
        """Test whether comparator returns a pandas DataFrame."""

        result = self._apply(self.data)
        assert isinstance(result, pd.DataFrame)

    def test_returns_frame_on_single_column(self):
        """
        Test whether comparator returns a pandas DataFrame even if only a
        single column is provided as input.
        """

        result = self._apply(self.data.iloc[:, [0]])
        assert isinstance(result, pd.DataFrame)

    def test_shape(self):
        """Test whether comparator returns DataFrame with same shape as input."""

        nrow = self.data.shape[0]
        result = self._apply(self.data)
        assert result.shape == (nrow, 1)

    def test_result(self):
        """Checker whether result matches the expected result."""

        result = self._apply(self.data)
        pd.testing.assert_frame_equal(result, self.expected)


class BaseComparatorTests:
    """Class providing basic unit tests for Comparator classes."""

    comparator = NotImplemented
    data = pd.DataFrame()
    target = NotImplemented
    expected = NotImplemented

    def _apply(self, df):
        """Applies a Comparator to a DataFrame."""

        comparator = Comparator.get(self.comparator)
        return comparator(df, target=self.target)

    def test_returns_frame(self):
        """Test whether comparator returns a pandas DataFrame."""

        result = self._apply(self.data)
        assert isinstance(result, pd.DataFrame)

    def test_returns_frame_on_single_column(self):
        """
        Test whether comparator returns a pandas DataFrame even if only a
        single column is provided as input.
        """

        result = self._apply(self.data.iloc[:, [0]])
        assert isinstance(result, pd.DataFrame)

    def test_shape(self):
        """Test whether comparator returns DataFrame with same shape as input."""

        result = self._apply(self.data)
        assert result.shape == self.data.shape

    def test_all_boolean(self):
        """Test whether comparator returns all boolean values."""

        result = self._apply(self.data)
        assert np.all(result.dtypes == bool)

    def test_result(self):
        """Checker whether result matches the expected result."""

        result = self._apply(self.data)
        pd.testing.assert_frame_equal(result, self.expected)
