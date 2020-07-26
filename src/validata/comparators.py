"""
Module providing Comparator classes used in the data validation tool.

Comparator classes perform logical comparisons to a provided target
value. Their `__call__()` method should accept a pandas DataFrame and
a comparison target value.

The method should compare all values in the DataFrame to the target and
return a DataFrame of identical shape containing only boolean values.

Comparator classes should always extend the `Comparators` base class and
be initialized via the `Comparators.get()` method.
"""

from validata.base_classes import Comparator


def _cast(target, value):
    """Try cast target to the same data type as value."""

    if isinstance(value, int):
        return int(target)

    if isinstance(value, float):
        return float(target)

    return target


class EqComparator(Comparator):
    """Checks for identical values."""

    symbol = "=="

    def __call__(self, df, target):
        return df.applymap(lambda x: x == _cast(target, x))


class UnEqComparator(Comparator):
    """Checks for non-identical values."""

    symbol = "!="

    def __call__(self, df, target):
        return df.applymap(lambda x: x != _cast(target, x))


class GtComparator(Comparator):
    """Checks whether the data is greater than the target."""

    symbol = ">"

    def __call__(self, df, target):
        return df.applymap(lambda x: x > float(target))


class GtEqComparator(Comparator):
    """Checks whether the data is greater than or equal to the target."""

    symbol = ">="

    def __call__(self, df, target):
        return df.applymap(lambda x: x >= float(target))


class LtComparator(Comparator):
    """Checks whether the data is less than the target."""

    symbol = "<"

    def __call__(self, df, target):
        return df.applymap(lambda x: x < float(target))


class LtEqComparator(Comparator):
    """Checks whether the data is less than or equal to the target."""

    symbol = "<="

    def __call__(self, df, target):
        return df.applymap(lambda x: x <= float(target))


class InComparator(Comparator):
    """Checks whether the data are present in the target list."""

    symbol = "in"

    def __call__(self, df, target):
        target = [t.strip() for t in target.split(",")]
        return df.applymap(lambda x: str(x) in target)


class BetweenComparator(Comparator):
    """Checks whether the data falls in the target range."""

    symbol = "between"

    def __call__(self, df, target):
        low, high = (float(t) for t in target.split(":"))
        return df.applymap(lambda x: low <= float(x) <= high)


class NullComparator(Comparator):
    """Checks whether the data is missing (no target required)."""

    symbol = "missing"

    def __call__(self, df, target=None):
        return df.isna()


class NotNullComparator(Comparator):
    """Checks whether the data is not missing (no target required)."""

    symbol = "not missing"

    def __call__(self, df, target=None):
        return ~df.isna()
