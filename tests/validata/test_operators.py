"""Module for unit testing Operator classes."""

import pandas as pd

from base_classes import BaseOperatorTests


# Dummy data for unit tests
DUMMY_DATA = pd.DataFrame(
    {
        "int": [1, 2, 3, 4],
        "int_miss": [4, None, 2, None],
        "bool": [True, True, False, False],
        "bool_miss": [True, False, None, None],
    }
)


class TestMeanOperator(BaseOperatorTests):
    """Tests for the MeanOperator class."""

    operator = "mean"
    data = DUMMY_DATA[["int", "int_miss"]]
    expected = pd.DataFrame({0: [2.5, 2.0, 2.5, 4.0]})


class TestMedianOperator(BaseOperatorTests):
    """Tests for the MedianOperator class."""

    operator = "median"
    data = DUMMY_DATA[["int", "int_miss"]]
    expected = pd.DataFrame({0: [2.5, 2.0, 2.5, 4.0]})


class TestMinOperator(BaseOperatorTests):
    """Tests for the MinOperator class."""

    operator = "min"
    data = DUMMY_DATA[["int", "int_miss"]]
    expected = pd.DataFrame({0: [1.0, 2.0, 2.0, 4.0]})


class TestMaxOperator(BaseOperatorTests):
    """Tests for the MaxOperator class."""

    operator = "max"
    data = DUMMY_DATA[["int", "int_miss"]]
    expected = pd.DataFrame({0: [4.0, 2.0, 3.0, 4.0]})


class TestSumOperator(BaseOperatorTests):
    """Tests for the SumOperator class."""

    operator = "sum"
    data = DUMMY_DATA[["int", "int_miss"]]
    expected = pd.DataFrame({0: [5.0, 2.0, 5.0, 4.0]})


class TestAnyOperator(BaseOperatorTests):
    """Tests for the AnyOperator class."""

    operator = "any"
    data = DUMMY_DATA[["bool", "bool_miss"]]
    expected = pd.DataFrame({0: [True, True, False, False]})


class TestAllOperator(BaseOperatorTests):
    """Tests for the AllOperator class."""

    operator = "all"
    data = DUMMY_DATA[["bool", "bool_miss"]]
    expected = pd.DataFrame({0: [True, False, False, False]})


class TestNoneOperator(BaseOperatorTests):
    """Tests for the NoneOperator class."""

    operator = "none"
    data = DUMMY_DATA[["bool", "bool_miss"]]
    expected = pd.DataFrame({0: [False, False, True, True]})
