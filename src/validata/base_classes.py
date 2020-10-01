"""Factory / base classes for Comparator and Operator classes."""

import numpy as np


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

    @staticmethod
    def _check_dtypes(df, dtype):
        """Check whether all columns match a certain data type."""

        invalid = set(df.columns) - set(df.select_dtypes(dtype))
        if invalid:
            raise TypeError(
                f"Columns did not match dtype '{dtype}': {', '.join(invalid)}."
            )

    @staticmethod
    def _cast(target, dtype):
        """
        Try cast target to the same data type as value.

        TODO:
        - Bit sloppy, needs improvement (object handling, error handling, etc)
        """

        if dtype in ["int", "int64"]:
            return int(target)

        if dtype in ["float", "float64"]:
            return float(target)

        if dtype == "bool":
            return bool(target)

        # Note: assuming string type for objects
        if dtype == "object":
            return str(target)

        if dtype == "datetime64[ns]":
            return np.datetime64(target)

        return target


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
