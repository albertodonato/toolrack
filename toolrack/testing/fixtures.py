"""Unit-test fixtures."""

import asyncio
from functools import (
    partial,
    wraps,
)
import os
from pathlib import Path
from shutil import rmtree
from tempfile import (
    mkdtemp,
    mkstemp,
)

import pytest


class Dir:
    """A helper for creating files and directories under a base directory.

    This is meant to be used for test fixtures.

    """

    def __init__(self, path: Path):
        self.path = path

    def __truediv__(self, other):
        """Append to the path."""
        return self.path / other

    def __str__(self):
        """The path as string."""
        return str(self.path)

    def join(self, *paths):
        """Join the specified path fragments with directory prefix."""
        return self.path.joinpath(*paths)

    def mkdir(self, path=None):
        """Create a temporary directory and return the :class:`pathlib.Path`.

        By default, a random name is chosen.

        :param path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.

        """
        return self._mkpath(path, mkdtemp, os.mkdir)

    def mkfile(self, path=None, content="", mode=None):
        """Create a temporary file and return the :class:`pathlib.Path`.

        By default, a random name is chosen.

        :param path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.
        :param str content: the content of the file.
        :param int mode: Unix permissions for the file.

        """
        path = self._mkpath(path, self._mkstemp, lambda p: Path(p).touch())

        if content:
            path.write_text(content)

        if mode is not None:
            path.chmod(mode)
        return path

    def mksymlink(self, target, path=None):
        """Create a symbolic link and return the :class:`pathlib.Path`.

        By default, a random name is chosen.

        :param target: path of the symlink target.
        :param path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.

        """
        return self._mkpath(
            path,
            partial(self._mkstemp_symlink, target),
            lambda p: Path(p).symlink_to(target),
        )

    def _mkpath(self, path, create_temp, create_func):
        if path is None:
            return Path(create_temp(dir=str(self.path)))

        if isinstance(path, tuple):
            path = Path().joinpath(*path)
        else:
            path = Path(path)
        if path.is_absolute():
            raise ValueError("Path must be relative")

        path = self.path / path
        # ensure parent exists
        path.parent.mkdir(parents=True, exist_ok=True)
        create_func(str(path))
        return path

    def _mkstemp(self, dir=None):
        fd, path = mkstemp(dir=dir)
        os.close(fd)
        return Path(path)

    def _mkstemp_symlink(self, target, dir=None):
        path = self._mkstemp(dir=dir)
        path.unlink()
        path.symlink_to(target)
        return path


@pytest.fixture
def tempdir(tmpdir):
    """A temporary directory fixture."""
    path = Path(mkdtemp(dir=str(tmpdir)))
    yield Dir(path)
    rmtree(str(path), ignore_errors=True)


@pytest.fixture
async def advance_time(event_loop):
    """Replace the loop clock with a manually advanceable clock.

    Code is taken from `asynctest.ClockedTestCase`.

    """

    class Clocker:
        time = 0

        def __init__(self, loop):
            self.loop = loop
            self.loop.time = wraps(self.loop.time)(lambda: self.time)

        async def advance(self, seconds):
            await self._drain_loop()

            target_time = self.time + seconds
            while True:
                next_time = self._next_scheduled()
                if next_time is None or next_time > target_time:
                    break

                self.time = next_time
                await self._drain_loop()

            self.time = target_time
            await self._drain_loop()

        def _next_scheduled(self):
            try:
                return self.loop._scheduled[0]._when
            except IndexError:
                return None

        async def _drain_loop(self):
            while True:
                next_time = self._next_scheduled()
                if not self.loop._ready and (
                    next_time is None or next_time > self.time
                ):
                    break
                await asyncio.sleep(0)

    yield Clocker(event_loop).advance
