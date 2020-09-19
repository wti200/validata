"""Module for unit testing Operator classes."""

import pandas as pd

from base_classes import BaseComparatorTests


# Dummy data for unit tests
DUMMY_DATA = pd.DataFrame(
    {
        "int": [1, 2, 3, 4],
        "int_miss": [1, None, 3, None],
        "float": [1.1, 2.2, 3.3, 4.4],
        "float_miss": [1.1, None, 3.3, None],
        "str": ["A", "B", "C", "D"],
        "str_miss": ["A", None, "C", None],
    }
)


class TestEqComparator(BaseComparatorTests):
    """Tests for the EqComparator class."""

    comparator = "=="
    data = DUMMY_DATA[["int", "int_miss", "str"]]
    target = 2
    expected = pd.DataFrame(
        {
            "int": [False, True, False, False],
            "int_miss": [False] * 4,
            "str": [False] * 4,
        }
    )


class TestUnEqComparator(BaseComparatorTests):
    """Tests for the EqComparator class."""

    comparator = "!="
    data = DUMMY_DATA[["int", "int_miss", "str"]]
    target = 2
    expected = pd.DataFrame(
        {"int": [True, False, True, True], "int_miss": [True] * 4, "str": [True] * 4}
    )


class TestGtComparator(BaseComparatorTests):
    """Tests for the GtComparator class."""

    comparator = ">"
    data = DUMMY_DATA[["int", "float", "int_miss"]]
    target = 2
    expected = pd.DataFrame(
        {
            "int": [False, False, True, True],
            "float": [False, True, True, True],
            "int_miss": [False, False, True, False],
        }
    )


class TestGtEqComparator(BaseComparatorTests):
    """Tests for the GtEqComparator class."""

    comparator = ">="
    data = DUMMY_DATA[["int", "float", "int_miss"]]
    target = 2
    expected = pd.DataFrame(
        {
            "int": [False, True, True, True],
            "float": [False, True, True, True],
            "int_miss": [False, False, True, False],
        }
    )


class TestLtComparator(BaseComparatorTests):
    """Tests for the LtComparator class."""

    comparator = "<"
    data = DUMMY_DATA[["int", "float", "int_miss"]]
    target = 3
    expected = pd.DataFrame(
        {
            "int": [True, True, False, False],
            "float": [True, True, False, False],
            "int_miss": [True, False, False, False],
        }
    )


class TestLtEqComparator(BaseComparatorTests):
    """Tests for the LtEqComparator class."""

    comparator = "<="
    data = DUMMY_DATA[["int", "float", "int_miss"]]
    target = 3
    expected = pd.DataFrame(
        {
            "int": [True, True, True, False],
            "float": [True, True, False, False],
            "int_miss": [True, False, True, False],
        }
    )


class TestInComparator(BaseComparatorTests):
    """Tests for the InComparator class."""

    comparator = "in"
    data = DUMMY_DATA[["int", "float", "str"]]
    target = "1, 1.1, A"
    expected = pd.DataFrame(
        {
            "int": [True, False, False, False],
            "float": [True, False, False, False],
            "str": [True, False, False, False],
        }
    )


class TestBetweenComparator(BaseComparatorTests):
    """Tests for the BetweenComparator class."""

    comparator = "between"
    data = DUMMY_DATA[["int", "float"]]
    target = "1:2"
    expected = pd.DataFrame(
        {"int": [True, True, False, False], "float": [True, False, False, False]}
    )


class TestNullComparator(BaseComparatorTests):
    """Tests for the NullComparator class."""

    comparator = "missing"
    data = DUMMY_DATA[["int_miss", "str_miss"]]
    target = None
    expected = pd.DataFrame(
        {
            "int_miss": [False, True, False, True],
            "str_miss": [False, True, False, True],
        }
    )


class TestNotNullComparator(BaseComparatorTests):
    """Tests for the NotNullComparator class."""

    comparator = "not missing"
    data = DUMMY_DATA[["int_miss", "str_miss"]]
    target = None
    expected = pd.DataFrame(
        {
            "int_miss": [True, False, True, False],
            "str_miss": [True, False, True, False],
        }
    )


class TestRankComparator(BaseComparatorTests):
    """Tests for the RankComparator class."""

    comparator = "ranks in"
    data = DUMMY_DATA[["int", "int_miss"]]
    target = "top 25 %"
    expected = pd.DataFrame(
        {"int": [False, False, False, True], "int_miss": [False] * 4}
    )


class TestContainsComparator(BaseComparatorTests):
    """Tests for the ContainsComparator class."""

    comparator = "contains"
    data = DUMMY_DATA[["str", "str_miss"]]
    target = "[ABC]+"
    expected = pd.DataFrame(
        {"str": [True, True, True, False], "str_miss": [True, False, True, False]}
    )


class TestOutlierComparator(BaseComparatorTests):
    """Tests for the OutlierComparator class."""

    comparator = "is outlier by"
    data = pd.DataFrame({"x": [-6, 8] + [0] * 10, "y": [40, None, None] + [0] * 9,})
    target = "2 SD"
    expected = pd.DataFrame(
        {"x": [True, True] + [False] * 10, "y": [True] + [False] * 11,}
    )
