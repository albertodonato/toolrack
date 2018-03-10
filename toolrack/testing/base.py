"""Base unit-test classes."""

from pathlib import Path
from unittest import TestCase as BaseTestCase

from fixtures import TestWithFixtures


class TestCase(TestWithFixtures, BaseTestCase):
    """Base class for tests."""

    def readfile(self, path):
        """Return the content of a file."""
        return Path(path).read_text()
