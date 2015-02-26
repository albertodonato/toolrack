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

from os import path

from collections import Iterable

from toolrack.path import match_files
from toolrack.testing import TestCase


class MatchFilesTests(TestCase):

    def test_return_iterator(self):
        '''The method returns an iterator.'''
        result = match_files(['dir'], ['match'])
        self.assertIsInstance(result, Iterable)

    def test_multiple_paths(self):
        '''The method returns matching files from all provided paths.'''
        dir1 = path.join(self.tempdir, 'dir1')
        dir2 = path.join(self.tempdir, 'dir2')
        self.mkfile(path=path.join(dir1, 'name'))
        self.mkfile(path=path.join(dir2, 'name'))
        self.assertItemsEqual(
            match_files([dir1, dir2], ['name']),
            [(dir1, 'name'), (dir2, 'name')])

    def test_glob_match(self):
        '''The method returns all files matching the pattern.'''
        self.mkfile(path='name1')
        self.mkfile(path='name2')
        self.assertItemsEqual(
            match_files([self.tempdir], ['name*']),
            [(self.tempdir, 'name1'), (self.tempdir, 'name2')])

    def test_multple_matches(self):
        '''The method returns files matching all patterns.'''
        self.mkfile(path='this-name')
        self.mkfile(path='other-name')
        self.mkfile(path='name1')
        self.assertItemsEqual(
            match_files([self.tempdir], ['name*', '*-name']),
            [(self.tempdir, 'this-name'), (self.tempdir, 'other-name'),
             (self.tempdir, 'name1')])

    def test_case_sensitive(self):
        '''The match is case sensitive by default.'''
        self.mkfile(path='name')
        self.mkfile(path='Name')
        self.mkfile(path='NAME')
        self.assertItemsEqual(
            match_files([self.tempdir], ['name']), [(self.tempdir, 'name')])

    def test_case_insensitive(self):
        '''The match can be made case insensitive.'''
        self.mkfile(path='name')
        self.mkfile(path='Name')
        self.mkfile(path='NAME')
        self.assertItemsEqual(
            match_files([self.tempdir], ['name'], ignorecase=True),
            [(self.tempdir, 'name'), (self.tempdir, 'Name'),
             (self.tempdir, 'NAME')])
