#
# This file is part of ToolRack.
#
# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Unit-test features.'''

import os
from tempfile import mkstemp, mkdtemp
from unittest import TestCase as BaseTestCase

from fixtures import TestWithFixtures, Fixture, TempDir


class TestCase(TestWithFixtures, BaseTestCase):
    '''Base class for tests.'''

    def readfile(self, path):
        '''Return the content of a file.'''
        with open(path) as fd:
            return fd.read()


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
            joined using :data:`os.path.sep`.

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
            joined using :data:`os.path.sep`.
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
