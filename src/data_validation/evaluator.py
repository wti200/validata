"""Module containing the Evaluator class for evaluating simple boolean expressions."""

import logging

from data_validation.tokenizer import Tokenizer
from data_validation.operators import Operators
from data_validation.comparators import Comparators

class Evaluator:
    """Evaluator class for parsing and evaluating simple boolean expressions."""

    def __init__(self, expression):
        self._log = logging.getLogger(__name__)

        # Construct token types
        token_types = {
            "COMPARATOR": Comparators.list(),
            "OPERATOR": Operators.list(),
        }
        self._tokenizer = Tokenizer(expression, token_types)

    def evaluate(self, df):
        """Evaluate the expression against the provided data frame."""

        result = df
        return result
