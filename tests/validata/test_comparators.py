"""Module for unit testing Operator classes."""

import pytest
import numpy as np
import pandas as pd

from validata.comparators import Comparator

COMPARATORS = Comparator.list()
TARGETS = {
    "in": "1, 2, 3, 4",
    "between": "0:100",
    "ranks in": "top 20%",
    "is outlier by": "1.5 IQR",
}


class TestComparators:
    """Class providing unit tests for Comparator classes."""

    @staticmethod
    def _apply_comparator(comparator, df):
        """Applies a Comparator to a DataFrame."""

        target = TARGETS.get(comparator, "0")
        comparator = Comparator.get(comparator)
        return comparator(df, target=target)

    @pytest.mark.parametrize("comparator", COMPARATORS)
    def test_returns_frame(self, comparator, dummy_data):
        """Test whether comparator returns a pandas DataFrame."""

        result = self._apply_comparator(comparator, dummy_data)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.parametrize("comparator", COMPARATORS)
    def test_returns_frame_on_single_column(self, comparator, dummy_data):
        """
        Test whether comparator returns a pandas DataFrame even if only a
        single column is provided as input.
        """

        result = self._apply_comparator(comparator, dummy_data)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.parametrize("comparator", COMPARATORS)
    def test_shape(self, comparator, dummy_data):
        """Test whether comparator returns DataFrame with same shape as input."""

        result = self._apply_comparator(comparator, dummy_data)
        assert result.shape == dummy_data.shape

    @pytest.mark.parametrize("comparator", COMPARATORS)
    def test_all_boolean(self, comparator, dummy_data):
        """Test whether comparator returns all boolean values."""

        result = self._apply_comparator(comparator, dummy_data)
        assert np.all(result.dtypes == bool)
