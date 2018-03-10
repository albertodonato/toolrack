"""Unit-test fixtures."""

import os
from pathlib import Path
from tempfile import (
    mkdtemp,
    mkstemp,
)

from fixtures import (
    Fixture,
    TempDir,
)


class TempDirFixture(Fixture):
    """Fixture providing a temporary base dir.

    The fixture also provides method to create sub-directories and files under
    the temporary directory.

    It's can be used in a :class:`fixtures.TestWithFixtures`::

      self.useFixture(TempDirFixture())

    """

    def setUp(self):
        """Set up a temporary directory."""
        super().setUp()
        self.path = Path(self.useFixture(TempDir()).path).absolute()

    def join(self, *paths):
        """Join the specified path fragments with directory prefix."""
        return self.path.joinpath(*paths)

    def mkdir(self, path=None):
        """Create a temporary directory and return the path.

        By default, a random name is chosen.

        :param path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.

        """
        return self._mkpath(path, mkdtemp, os.mkdir)

    def mkfile(self, path=None, content='', mode=None):
        """Create a temporary file and return its path.

        By default, a random name is chosen.

        :param path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.
        :param str content: the content of the file.
        :param int mode: Unix permissions for the file.

        """
        path = self._mkpath(path, self._mkstemp, self._touch)

        if content:
            path.write_text(content)

        if mode is not None:
            path.chmod(mode)
        return path

    def _mkpath(self, path, create_temp, create_func):
        if path is None:
            return Path(create_temp(dir=self.path))

        if isinstance(path, tuple):
            path = Path().joinpath(*path)
        else:
            path = Path(path)
        if path.is_absolute():
            raise ValueError('Path must be relative')

        path = self.path / path
        # ensure parent exists
        path.parent.mkdir(parents=True, exist_ok=True)
        create_func(path)
        return path

    def _mkstemp(self, **kwargs):
        fd, path = mkstemp(**kwargs)
        os.close(fd)
        return Path(path)

    def _touch(self, path):
        path.touch()
