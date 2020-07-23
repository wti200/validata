"""Module containing a Tokenizer class for boolean expressions."""

import re
import logging


class Token:
    """Class for a single token."""

    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    """
    Iterator class for tokenizing a string expression.

    Parameters
    ----------
    expression : str
        Expression to generate tokens from.
    tokens : dict
        Mapping between tokens and their symbols / string representations.
    bare_words : Optional[str]
        Specify handling of bare words:
        - "capture": capture bare words as tokens (default)
        - "drop": drop bare words and return tokens only
        - "error": raise an error when encountering a bare word
    case_sensitive : Optional[bool]
        Perform case sensitive matching or not (default)
    """

    _pointer = 0
    _tokens = []

    def __init__(self, expression, tokens, bare_words="capture", case_sensitive=False):
        self._log = logging.getLogger(__name__)

        expression = expression.strip()
        if not expression or not isinstance(expression, str):
            raise ValueError("Please provide an expression as string.")

        if not tokens or not isinstance(tokens, dict):
            raise ValueError("Please provide a dict of token types.")

        if bare_words not in ["capture", "drop", "error"]:
            raise ValueError(f"Invalid bare_words option provided: {bare_words}")

        self._bare_words = bare_words
        self._case_sensitive = case_sensitive

        self._lookup = self._build_lookup(tokens)
        self._tokens = self._tokenize(expression)

    def _build_lookup(self, token_types):
        """Build symbol to label lookup dict."""

        lookup = {}
        for label, symbols in token_types.items():
            if not isinstance(symbols, (set, list, tuple)):
                symbols = [symbols]

            for symbol in symbols:
                if not self._case_sensitive:
                    symbol = symbol.lower()
                lookup.update({symbol: label})

        return lookup

    def _tokenize(self, expression):
        """Tokenize the expression."""

        types_str = r"\b|\b".join([re.escape(symbol) for symbol in self._lookup])
        types_str = r"(\b{0}\b)".format(types_str)
        if self._case_sensitive:
            split_reg = re.compile(types_str)
        else:
            split_reg = re.compile(types_str, re.IGNORECASE)

        tokens = []
        for symbol in split_reg.split(expression):
            # Skip empty tokens
            symbol = symbol.strip()
            if not symbol:
                continue

            # Bare word encountered
            lookup = symbol if self._case_sensitive else symbol.lower()
            if lookup not in self._lookup:
                if self._bare_words == "capture":
                    tokens.append(Token("BARE WORD", symbol))

                elif self._bare_words == "error":
                    raise ValueError(f"Encountered bare word in expression: {symbol}.")

            # Token encountered
            else:
                tokens.append(Token(self._lookup[lookup], symbol))

        return tokens

    def peek(self):
        """Peeks ahead at the next token."""

        if self.has_next():
            return self._tokens[self._pointer + 1]
        return None

    def has_next(self):
        """Checks whether there is a next token."""

        return self._pointer < len(self._tokens)

    def reset(self):
        """Resets the pointer to the starting token."""

        self._pointer = 0

    def __iter__(self):
        """Start iteration, resets the pointer."""

        self._pointer = 0
        return self

    def __next__(self):
        """Returns the next token."""

        if not self.has_next():
            raise StopIteration

        token = self._tokens[self._pointer]
        self._pointer += 1
        return token
