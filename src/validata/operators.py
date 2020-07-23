"""
Module providing Operator classes used in the data validation tool.

Operator classes perform aggregations to reduce multiple columns to a
single one. Therefore the `__call__()` method of an Operater should
accept a DataFrame with 1 or more columns and return a DataFrame
with just a single column.

Operator classes should extend either the DataOperator or LogicalOperator
base class. DataOperator classes operate on the raw data values; for example,
they could compute the sum or the minimum value from a set of columns.

LogicalOperators operate on the boolean values returned by a Comparator. A
Comparator can return multiple columns with boolean values. A LogicalOperator
should reduce those to a single column, for example, by checking whether all
values are True.

All Operator classes should be initialized using the `Operator.get()` method.
"""

# pylint: disable=unused-import
from validata.base_classes import Operator, DataOperator, LogicalOperator


class MeanOperator(DataOperator):
    """Computes the mean value across columns."""

    symbol = "mean"

    def __call__(self, df):
        return df.mean(axis=1).to_frame()


class MedianOperator(DataOperator):
    """Computes the median value across columns."""

    symbol = "median"

    def __call__(self, df):
        return df.median(axis=1).to_frame()


class MinOperator(DataOperator):
    """Computes the minumum value across columns."""

    symbol = "min"

    def __call__(self, df):
        return df.min(axis=1).to_frame()


class MaxOperator(DataOperator):
    """Computes the maximum value across columns."""

    symbol = "max"

    def __call__(self, df):
        return df.max(axis=1).to_frame()


class SumOperator(DataOperator):
    """Computes the sum across columns."""

    symbol = "sum"

    def __call__(self, df):
        return df.sum(axis=1).to_frame()


class AnyOperator(LogicalOperator):
    """Returns True if any column contains True, False otherwise."""

    symbol = "any"

    def __call__(self, df):
        return df.any(axis=1).to_frame()


class AllOperator(LogicalOperator):
    """Returns True if all columns contain True, False otherwise."""

    symbol = "all"

    def __call__(self, df):
        return df.all(axis=1).to_frame()


class NoneOperator(LogicalOperator):
    """Returns True if all column contain False, True otherwise."""

    symbol = "none"

    def __call__(self, df):
        return ~df.any(axis=1).to_frame()
