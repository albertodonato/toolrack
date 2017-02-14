'''Unit-test fixtures.'''

import os
from tempfile import mkstemp, mkdtemp

from fixtures import Fixture, TempDir


class TempDirFixture(Fixture):
    '''Fixture providing a temporary base dir.

    The fixture also provides method to create sub-directories and files under
    the temporary directory.

    It's can be used in a :class:`fixtures.TestWithFixtures`::

      self.useFixture(TempDirFixture())

    '''

    def setUp(self):
        '''Set up a temporary directory.'''
        super().setUp()
        self.path = self.useFixture(TempDir()).path

    def join(self, *paths):
        '''Join the specified path fragments with directory prefix.'''
        return os.path.join(self.path, *paths)

    def mkdir(self, path=None):
        '''Create a temporary directory and return the path.

        By default, a random name is chosen.

        Parameters:
          - path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.

        '''
        return self._mkpath(path, mkdtemp, os.mkdir)

    def mkfile(self, path=None, content='', mode=None):
        '''Create a temporary file and return its path.

        By default, a random name is chosen.

        Parameters:
          - path: if specified, it's appended to the base directory and all
            intermiediate directories are created too.
            A relative path *must* be specified.
            A tuple of strings can be also passed, in which case elements are
            joined using :func:`os.path.sep`.
          - content: the content of the file.
          - mode: Unix permissions for the file.

        '''
        path = self._mkpath(path, self._mkstemp, self._touch)

        if content:
            with open(path, 'w') as fh:
                fh.write(content)

        if mode is not None:
            os.chmod(path, mode)
        return path

    def _mkpath(self, path, create_temp, create_func):
        if path is None:
            return create_temp(dir=self.path)

        if isinstance(path, tuple):
            path = os.path.join(*path)
        if os.path.isabs(path):
            raise ValueError('Path must be relative.')

        path = os.path.join(self.path, path)
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        create_func(path)
        return path

    def _mkstemp(self, **kwargs):
        fd, path = mkstemp(**kwargs)
        os.close(fd)
        return path

    def _touch(self, path):
        fd = open(path, 'w')
        fd.close()
