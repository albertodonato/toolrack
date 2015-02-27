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
from tempfile import mktemp
from unittest import TestCase as BaseTestCase

from fixtures import TestWithFixtures, TempDir


class TestCase(TestWithFixtures, BaseTestCase):
    '''Base class for tests.'''

    def setUp(self):
        super(TestCase, self).setUp()
        # A base temporary directory
        self.tempdir = self.useFixture(TempDir()).path

    def mkdir(self):
        '''Create a temporary directory and return the path.'''
        fixture = self.useFixture(TempDir(rootdir=self.tempdir))
        return fixture.path

    def mkfile(self, path=None, content='', mode=None):
        '''Create a temporary file and return its path.

        if path is specified, it's appended to tempdir and all intermiediate
        directories are created.

        '''
        if path is None:
            path = mktemp(dir=self.tempdir)
        else:
            path = os.path.join(self.tempdir, path)
            dir_path = os.path.dirname(path)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

        with open(path, 'w') as fh:
            fh.write(content)

        if mode is not None:
            os.chmod(path, mode)
        return path
