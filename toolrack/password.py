"""Password generation functions.

:class:`PasswordProfile` defines a set of characters to use for generating
password.  It's creating by passing a string with characters or character
definitions encosed in curly braces (such as ``{alnum}``, ``{num}``,
``{alpha}``), which are expanded to the corresponding set of characters.

For instance::

 profile = PasswordProfile('{alpha}-_')
 profile.generate(length=5)

yields a 5-chars password composed of letters, dashes and underscores.

"""

from random import SystemRandom
import string

#: Default character set: letters, numbers and punctuation
DEFAULT_CHARS = string.ascii_letters + string.digits + string.punctuation
#: Default password length
DEFAULT_LENGTH = 10


def generate_password(chars=DEFAULT_CHARS, length=DEFAULT_LENGTH):
    """Generate a random password using the supplied characters.

    :param str chars: a string with chars to choose from.
    :param int length: number of chars for the password.

    """
    random = SystemRandom()
    return "".join(random.choice(chars) for _ in range(length))


class PasswordProfile:
    """A password profile, specifying how to generate a random password."""

    CHAR_DEFS = {
        "alnum": string.ascii_letters + string.digits,
        "alpha": string.ascii_letters,
        "num": string.digits,
        "space": string.whitespace,
        "punct": string.punctuation,
    }

    def __init__(self, definition):
        self.definition = definition
        self._chars = self._get_chars()

    @property
    def chars(self):
        """Return the set of characters used in generation."""
        return self._chars

    def generate(self, length=DEFAULT_LENGTH):
        """Generate a random password."""
        return generate_password(chars=self._chars, length=length)

    def _get_chars(self):
        """Return a list of chars from a definition."""
        chars_def = self.definition
        for tag, chars in self.CHAR_DEFS.items():
            chars_def = chars_def.replace(f"{{{tag}}}", chars)
        # remove duplicates
        return "".join(set(chars_def))
