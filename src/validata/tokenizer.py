"""Module containing a Tokenizer class for boolean expressions."""

import string
import logging


class Token:
    """Class for a single token."""

    def __init__(self, token_value, token_type):
        self.value = token_value
        self.type = token_type

    def __repr__(self):
        return f"Token({self.value}, {self.type})"


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
    }

    # Define quoting styles
    _quote_styles = {
        "'": "QUOTED STRING",
        '"': "QUOTED STRING",
        "`": "REGEX",
    }

    # Define word boundary and punctuation characters
    _word_boundary = string.whitespace + "()<>=&|"
    _punctuation = string.punctuation

    # Initialize variables
    _tokens = []
    _lookup = []
    _pointer = 0

    def __init__(self, expression, additional_types=None):
        self._log = logging.getLogger(__name__)

        # Update tokens
        if additional_types:
            self._token_types.update(additional_types)

        # Tokenize the expression
        self._lookup = sorted(self._token_types, key=len, reverse=True)
        self._tokens = self._tokenize(expression)
        self._pointer = 0

    def _tokenize(self, expression):
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

        tokens = []
        while expression:

            # Check for a token
            token, expression = self._capture_token(expression)
            if token:
                self._log.debug("Found token: %s [%s]", token.value, token.type)
                tokens.append(token)

            # Quoted string
            elif expression[0] in self._quote_styles:
                quote_style = self._quote_styles[expression[0]]
                quoted_str, expression = self._capture(
                    expression[1:], exclude=expression[0]
                )
                expression = expression[1:]
                self._log.debug("Found quoted string: %s [%s]", quoted_str, quote_style)
                tokens.append(Token(quoted_str, quote_style))

            # Word characters
            elif expression[0] not in self._word_boundary:
                word_str, expression = self._capture(
                    expression, exclude=self._word_boundary
                )
                self._log.debug("Found word: %s", word_str)
                tokens.append(Token(word_str, "WORD"))

            # Punctuation
            elif expression[0] in self._punctuation:
                punctuation_str, expression = self._capture(
                    expression, include=self._punctuation
                )
                self._log.debug("Found punctuation: %s", punctuation_str)
                tokens.append(Token(punctuation_str, "PUNCTUATION"))

            # Skip
            else:
                self._log.debug("Ignored character: '%s'", expression[0])
                expression = expression[1:]

        return tokens

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
            elif include and expression[0] not in include:
                break
            elif exclude and expression[0] in exclude:
                break
            captured += expression[0]
            expression = expression[1:]

        return captured, expression

    def peek(self):
        """Peeks ahead at the next token."""

        if self.has_next():
            return self._tokens[self._pointer]
        return None

    # pylint: disable=invalid-name
    def rewind(self, by=1):
        """Rewinds pointer to the previous token."""

        if self._pointer < by:
            raise ValueError(
                f"Cannot rewind tokenizer by {by} tokens; not enough tokens."
            )
        self._pointer -= by

    def has_next(self):
        """Checks whether there are more tokens."""

        return self._pointer < len(self._tokens)

    def __iter__(self):
        """Start iteration, resets the pointer."""

        return self

    def __next__(self):
        """Returns the next token."""

        if not self.has_next():
            # self._pointer = 0
            raise StopIteration

        token = self._tokens[self._pointer]
        self._pointer += 1
        return token
