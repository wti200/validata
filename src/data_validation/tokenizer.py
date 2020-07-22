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
    token_types : dict
        Mapping between tokens and their string representations.
    bare_words : Optional[str]
        Specify handling of bare words:
        - "capture": capture bare words as tokens (default)
        - "drop": drop bare words and return tokens only
        - "error": raise an error when encountering a bare word
    case_sensitive : Optional[bool]
        Perform case sensitive matching or not (default)
    """

    _tokens = []

    def __init__(self, expression, token_types, bare_words="capture", case_sensitive=False):
        self._log = logging.getLogger(__name__)

        expression = expression.strip()
        if not expression or not isinstance(expression, str):
            raise ValueError("Please provide an expression as string.")

        if not token_types or not isinstance(token_types, dict):
            raise ValueError("Please provide a dict of token types.")

        if bare_words not in ["capture", "drop", "error"]:
            raise ValueError(f"Invalid bare_words option provided: {bare_words}")

        self._expression = expression
        self._types = token_types
        self._bare_words = bare_words
        self._case_sensitive = case_sensitive

        self._lookup = self._build_lookup()
        self._tokens = self._tokenize()

    def _build_lookup(self):
        """Build symbol to label lookup dict."""

        lookup = {}
        for label, symbols in self._types.items():
            if not isinstance(symbols, (set, list, tuple)):
                symbols = [symbols]

            for symbol in symbols:
                if not self._case_sensitive:
                    symbol = symbol.lower()
                lookup.update({symbol: label})

        return lookup

    def _tokenize(self):
        """Tokenize the expression."""

        types_str = "|".join([re.escape(symbol) for symbol in self._lookup])
        if self._case_sensitive:
            split_reg = re.compile(r"(" + types_str + r")")
        else:
            split_reg = re.compile(r"(" + types_str + r")", re.IGNORECASE)

        tokens = []
        for symbol in split_reg.split(self._expression):
            # Cleanse and handle case
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

            else:
                tokens.append(Token(self._lookup[lookup], symbol))

        return tokens

    def peek(self):
        """Peeks ahead at the next token."""

        if self.has_next():
            return self._tokens[0]
        return None

    def has_next(self):
        """Checks whether there is a next token."""

        return len(self._tokens) > 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """Returns the next token."""

        while self._tokens:
            return self._tokens.pop(0)
        raise StopIteration
