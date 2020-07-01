"""
Module providing Operator classes used in the data validation tool.

Comparator classes perform aggregations to reduce data frames to a
single column. They can be used either before or after a Comparator
class is applied. The `__call__()` method of an Operater should accept
a pandas DataFrame and return a DataFrame with only a single column.

Operator classes should always extend the `Operators` base class and
be initialized via the `Operators.get()` method.
"""


class Operators:
    """Abstract factory class for initializing Operator objects."""

    apply = "before"

    @classmethod
    def get(cls, name):
        """
        Method for getting a Operator object based on its name.

        Parameters
        ==========
        tag : str
            String identifying a Operator, for example "mean".

        Returns
        =======
        Comparator
            Instance of an Operator subclass
        """

        op_name = f"{name.capitalize()}Operator"
        operators = {op.__name__: op for op in cls.__subclasses__()}
        if op_name not in operators:
            raise TypeError(f"Undefined operator: {name}.")

        return operators[op_name]()

    @classmethod
    def list(cls):
        """Returns a set of available Operator names."""

        # Strip "Operator" from class name
        return {op.__name__[:-8].lower() for op in cls.__subclasses__()}


class MeanOperator(Operators):
    """Computes the mean value across columns."""

    def __call__(self, df):
        return df.mean(axis=1).to_frame()


class MedianOperator(Operators):
    """Computes the median value across columns."""

    def __call__(self, df):
        return df.median(axis=1).to_frame()


class MinOperator(Operators):
    """Computes the minumum value across columns."""

    def __call__(self, df):
        return df.min(axis=1).to_frame()


class MaxOperator(Operators):
    """Computes the maximum value across columns."""

    def __call__(self, df):
        return df.max(axis=1).to_frame()


class SumOperator(Operators):
    """Computes the sum across columns."""

    def __call__(self, df):
        return df.sum(axis=1).to_frame()


class AnyOperator(Operators):
    """Returns True if any column contains True, False otherwise."""

    apply = "after"

    def __call__(self, df):
        return df.any(axis=1).to_frame()


class AllOperator(Operators):
    """Returns True if all columns contain True, False otherwise."""

    apply = "after"

    def __call__(self, df):
        return df.all(axis=1).to_frame()


class NoneOperator(Operators):
    """Returns True if all column contain False, True otherwise."""

    apply = "after"

    def __call__(self, df):
        return ~df.any(axis=1).to_frame()
