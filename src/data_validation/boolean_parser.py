"""Module containing the BooleanParser class for parsing complex boolean expressions."""

import logging

from data_validation.tokenizer import Tokenizer
from data_validation.evaluator import Evaluator


class BooleanParser:
    """Parses nested boolean expressions."""

    token_types = {
        "AND": ["and", "en", "&"],
        "OR":  ["or", "of", "|"],
        "GROUP_OPEN": "(",
        "GROUP_CLOSE": ")",
    }

    def __init__(self, expression):
        self._log = logging.getLogger(__name__)
        self._tokenizer = Tokenizer(expression, self.token_types)

    def evaluate(self, variables):
        """Evaluate boolean expression using a dict of variables: values."""

        result = None

        for token in self._tokenizer:

            self._log.debug("Processing token: %s", token.value)

            # Handle grouping / nesting
            if token.type == "GROUP_OPEN":
                self._log.debug("Entering nested expression.")
                result = self.evaluate(variables)

            elif token.type == "GROUP_CLOSE":
                self._log.debug("Exiting nested expression.")
                break

            elif token.type in ["AND", "OR"]:
                self._log.debug("Processing %s expression.", token.value)

                if result is None:
                    raise ValueError(
                        "Use of and / or without left hand side expression."
                    )

                # Get right hand side, compute results
                next_token = next(self._tokenizer)
                if next_token.type == "GROUP_OPEN":
                    self._log.debug("Processing token: %s", next_token.value)
                    self._log.debug("Entering nested right hand side expression.")
                    right_hand = self.evaluate(variables)

                else:
                    self._log.debug("Processing token: %s", next_token.value)
                    self._log.debug("Evaluating right hand side expression.")
                    right_hand = Evaluator(next_token.value).evaluate(variables)

                # Apply and / or operation
                if token.type == "AND":
                    result = result and right_hand
                else:
                    result = result or right_hand

            else:
                self._log.debug("Evaluating expression: %s", token.value)

                if result is not None:
                    raise ValueError("Expected and / or, got expression instead.")

                result = Evaluator(token.value).evaluate(variables)

        return result
