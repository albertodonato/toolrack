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

from os import path

from toolrack.testing import TestCase, TempDirFixture
from toolrack.fsmap import Directory, DIR


class DirectoryTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = self.useFixture(TempDirFixture())
        self.dir = Directory(self.tempdir.path)

    def test_iter_list_files(self):
        '''Iterating on the Directory returns contained file names.'''
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        self.assertCountEqual(['bar', 'foo'], self.dir)

    def test_getitem_reads_file(self):
        '''Accessing a file item returns the content.'''
        self.tempdir.mkfile(path='foo', content='some foo')
        self.assertEqual(self.dir['foo'], 'some foo')

    def test_getitem_returns_directory(self):
        '''Accessing a file item returns the content.'''
        dir_path = self.tempdir.mkdir()
        self.assertIsInstance(self.dir[path.basename(dir_path)], Directory)

    def test_getitem_traverses_paths(self):
        '''It's possible to traverse subdirectories when accessing elements.'''
        file_path = path.join('subdir', 'file')
        self.tempdir.mkfile(path=file_path, content='some content')
        self.assertEqual(self.dir[file_path], 'some content')

    def test_getitem_notfound_raises(self):
        '''An error is raised if the element is not found.'''
        self.assertRaises(KeyError, self.dir.__getitem__, 'unknown')

    def test_setitem_writes_file(self):
        '''Setting an element writes the file.'''
        self.dir['foo'] = 'some content'
        self.assertEqual(
            self.readfile(path.join(self.tempdir.path, 'foo')), 'some content')

    def test_setitem_creates_directory(self):
        '''Setting an item to DIR creates the directory.'''
        self.dir['foo'] = DIR
        self.assertTrue(path.isdir(path.join(self.tempdir.path, 'foo')))

    def test_delitem_removes_file(self):
        '''Deeleting an item removes the corresponding file.'''
        self.tempdir.mkfile(path='foo')
        del self.dir['foo']
        self.assertFalse(path.exists(path.join(self.tempdir.path, 'foo')))

    def test_delitem_removes_directory(self):
        '''Deeleting an item removes the corresponding directory.'''
        dir_path = self.tempdir.mkdir()
        del self.dir[path.basename(dir_path)]
        self.assertFalse(path.exists(dir_path))
