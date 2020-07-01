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


class Comparators:
    """Abstract factory class for initializing Comparator objects."""

    @classmethod
    def get(cls, tag):
        """
        Method for getting a Comparator object based on its tag.

        Parameters
        ==========
        tag : str
            String identifying a comparator, for example "==".

        Returns
        =======
        Comparator
            Instance of a comparator subclass
        """

        tags = {comp.tag: comp for comp in cls.__subclasses__()}
        if tag not in tags:
            raise TypeError(f"Undefined comparator: {tag}.")

        return tags[tag]()

    @classmethod
    def list(cls):
        """Returns a set of available Comparator tags."""

        return {comp.tag for comp in cls.__subclasses__()}


class EqComparator(Comparators):
    """Checks for identical values."""

    tag = "=="

    def __call__(self, df, target):
        return df.applymap(lambda x: x == target)


class UnEqComparator(Comparators):
    """Checks for non-identical values."""

    tag = "!="

    def __call__(self, df, target):
        return df.applymap(lambda x: x != target)


class GtComparator(Comparators):
    """Checks whether the data is greater than the target."""

    tag = ">"

    def __call__(self, df, target):
        return df.applymap(lambda x: x > float(target))


class GtEqComparator(Comparators):
    """Checks whether the data is greater than or equal to the target."""

    tag = ">="

    def __call__(self, df, target):
        return df.applymap(lambda x: x >= float(target))


class LtComparator(Comparators):
    """Checks whether the data is less than the target."""

    tag = "<"

    def __call__(self, df, target):
        return df.applymap(lambda x: x < float(target))


class LtEqComparator(Comparators):
    """Checks whether the data is less than or equal to the target."""

    tag = "<="

    def __call__(self, df, target):
        return df.applymap(lambda x: x <= float(target))


class InComparator(Comparators):
    """Checks whether the data are present in the target list."""

    tag = "in"

    def __call__(self, df, target):
        target = [t.strip() for t in target.split(",")]
        return df.applymap(lambda x: str(x) in target)


class BetweenComparator(Comparators):
    """Checks whether the data falls in the target range."""

    tag = "between"

    def __call__(self, df, target):
        low, high = (float(t) for t in target.split(":"))
        return df.applymap(lambda x: low <= float(x) <= high)


class NullComparator(Comparators):
    """Checks whether the data is missing (no target required)."""

    tag = "missing"

    def __call__(self, df, target=None):
        return df.isna()


class NotNullComparator(Comparators):
    """Checks whether the data is not missing (no target required)."""

    tag = "not missing"

    def __call__(self, df, target=None):
        return ~df.isna()
