"""Module containing a Tokenizer class for boolean expressions."""

import string
import logging


class Token:
    """Class for a single token."""

    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    """
    Class for tokenizing a logical string expression.

    Parameters
    ----------
    expression : str
        Expression to generate tokens from.
    """

    # Define token types
    _token_types = {
        "(": "GROUP_OPEN",
        ")": "GROUP_CLOSE",
        "&": "AND",
        "|": "OR",
        "is": "EqualComparator",
        "is missing": "MissingComparator",
        "==": "EqualComparator",
    }

    # Define quoting styles
    _quote_styles = {
        "'": "QUOTED STRING",
        '"': "QUOTED STRING",
        "`": "REGEX",
    }

    # Define word boundaries
    _word_boundary = string.whitespace + "()<>=&|"

    _pointer = 0
    _tokens = []
    _tmp = ""

    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._lookup = sorted(self._token_types, key=len, reverse=True)

    def tokenize(self, expression):
        """
        Generator for tokenizing a logical string.

        Parameters
        ----------
        expression : str
            Expression to generate tokens from.

        Returns
        -------
        Iterator
            Iterator returning tokens from the logical expression.
        """

        while expression:

            # Check for a token
            token, expression = self._capture_token(expression)
            if token:
                self._log.debug("Found token: %s [%s]", token.value, token.type)
                yield token

            # Quoted string
            elif expression[0] in self._quote_styles:
                quote_style = self._quote_styles[expression[0]]
                quoted_str, expression = self._capture(
                    expression[1:], exclude=expression[0]
                )
                expression = expression[1:]
                self._log.debug("Found quoted string: %s [%s]", quoted_str, quote_style)
                yield Token(quoted_str, quote_style)

            # Anything except whitespace
            elif expression[0] not in string.whitespace:
                word_str, expression = self._capture(
                    expression, exclude=self._word_boundary
                )
                self._log.debug("Found word: %s", word_str)
                yield Token(word_str, "WORD")

            # Skip
            else:
                expression = expression[1:]

    def _capture_token(self, expression):
        """
        Searches for and captures tokens from a logical expression.

        Parameters
        ----------
        expression : str
            Expression to capture the substring from.

        Returns
        -------
        Tuple[str, str]
            Tuple of captured string and remainder of the logical expression.
        """

        for token in self._lookup:
            if expression.startswith(token):
                return Token(token, self._token_types[token]), expression[len(token) :]
        return None, expression

    @staticmethod
    def _capture(expression, exclude=None, include=None):
        """
        Captures a substring from a logical expression.

        Parameters
        ----------
        expression : str
            Expression to capture the substring from.
        exclude : Union[list, str]
            List or string of characters that end the substring pattern.
        include : Union[list, str]
            List or string of characters that should be included in the substring.

        Returns
        -------
        Tuple[str, str]
            Tuple of captured string and remainder of the logical expression.
        """

        captured = ""
        while expression:
            if expression[0] == "\\":
                expression = expression[1:]
            elif include and expression[0] not in exclude:
                break
            elif exclude and expression[0] in exclude:
                break
            captured += expression[0]
            expression = expression[1:]

        return captured, expression
