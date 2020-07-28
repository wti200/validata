"""Factory / base classes for Comparator and Operator classes."""


class Comparator:
    """Abstract factory class for initializing Comparator objects."""

    @classmethod
    def get(cls, symbol):
        """
        Method for getting a Comparator object based on its symbol.

        Parameters
        ----------
        symbol : str
            String (lower case) identifying a comparator, for example "==".

        Returns
        -------
        Comparator
            Instance of the requested Comparator subclass.
        """

        symbols = {comp.symbol: comp for comp in cls.__subclasses__()}
        if symbol not in symbols:
            raise TypeError(f"Unknown Comparator: {symbol}.")

        return symbols[symbol]()

    @classmethod
    def list(cls):
        """Returns a set of available Comparator symbols."""

        return {comp.symbol for comp in cls.__subclasses__()}


class Operator:
    """Abstract factory class for initializing Operator objects."""

    @classmethod
    def get(cls, symbol):
        """
        Method for getting a Operator object based on its symbol.

        Parameters
        ----------
        symbol : str
            String (lower case) identifying a comparator, for example "mean".

        Returns
        -------
        Operator
            Instance of the requested Operator subclass.
        """

        symbols = {
            op.symbol: op for op in cls.get_subclasses() if hasattr(op, "symbol")
        }
        if symbol not in symbols:
            raise TypeError(f"Unknown Operator: {symbol}.")

        return symbols[symbol]()

    @classmethod
    def list(cls):
        """
        Returns a set of available Comparator symbols.

        Returns
        -------
        set
            Set of available Comparator symbols
        """

        return {op.symbol for op in cls.get_subclasses() if hasattr(op, "symbol")}

    @classmethod
    def get_subclasses(cls):
        """Returns all subclasses recursively."""

        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass


class DataOperator(Operator):
    """Base class for data operators."""


class LogicalOperator(Operator):
    """Base class for logical operators."""
