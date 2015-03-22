#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Unittest classes.'''

import os
from tempfile import mkstemp, mkdtemp
from unittest import TestCase as BaseTestCase

from fixtures import TestWithFixtures, Fixture, TempDir


class TestCase(TestWithFixtures, BaseTestCase):
    '''Base class for tests.'''

    def setUp(self):
        super(TestCase, self).setUp()
        # A base temporary directory
        self.tempdir = self.useFixture(TempDir()).path

    def readfile(self, path):
        '''Return the content of a file.'''
        with open(path) as fd:
            return fd.read()


class TempDirFixture(Fixture):

    def setUp(self):
        super(TempDirFixture, self).setUp()
        self.path = self.useFixture(TempDir()).path

    def mkdir(self, path=None):
        '''Create a temporary directory and return the path.

        If a path is specified, it's appended to tempdir and all intermiediate
        directories are created.  The path attribute can be a tuple, in which
        case elements are joined.

        '''
        return self._mkpath(path, mkdtemp)

    def mkfile(self, path=None, content='', mode=None):
        '''Create a temporary file and return its path.

        If path is specified, it's appended to tempdir and all intermiediate
        directories are created.

        '''
        path = self._mkpath(path, mkstemp)

        with open(path, 'w') as fh:
            fh.write(content)

        if mode is not None:
            os.chmod(path, mode)
        return path

    def _mkpath(self, path, create_func):
        if path is None:
            path = create_func(dir=self.path)
        else:
            if isinstance(path, tuple):
                path = os.path.join(*path)
            if os.path.isabs(path):
                raise ValueError('Path must be relative.')

            path = os.path.join(self.path, path)
            dirname = os.path.dirname(path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
        return path
