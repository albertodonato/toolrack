from os import path
from pathlib import Path

from ..testing import TestCase
from ..testing.fixtures import TempDirFixture
from ..fsmap import Directory, DIR


class DirectoryTests(TestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = self.useFixture(TempDirFixture())
        self.dir = Directory(self.tempdir.path)

    def test_iter_list_files(self):
        """Iterating on the Directory returns contained file names."""
        self.tempdir.mkfile(path='foo')
        self.tempdir.mkfile(path='bar')
        self.assertCountEqual(
            self.dir,
            [self.tempdir.path / 'bar', self.tempdir.path / 'foo'])

    def test_getitem_reads_file(self):
        """Accessing a file item returns the content."""
        self.tempdir.mkfile(path='foo', content='some foo')
        self.assertEqual(self.dir['foo'], 'some foo')

    def test_getitem_returns_directory(self):
        """Accessing a file item returns the content."""
        dir_path = self.tempdir.mkdir()
        self.assertIsInstance(self.dir[dir_path.name], Directory)

    def test_getitem_traverses_paths(self):
        """It's possible to traverse subdirectories when accessing elements."""
        file_path = path.join('subdir', 'file')
        self.tempdir.mkfile(path=file_path, content='some content')
        self.assertEqual(self.dir[file_path], 'some content')

    def test_getitem_notfound_raises(self):
        """An error is raised if the element is not found."""
        self.assertRaises(KeyError, self.dir.__getitem__, 'unknown')

    def test_setitem_writes_file(self):
        """Setting an element writes the file."""
        self.dir['foo'] = 'some content'
        self.assertEqual(
            (self.tempdir.path / 'foo').read_text(), 'some content')

    def test_setitem_creates_directory(self):
        """Setting an item to DIR creates the directory."""
        self.dir['foo'] = DIR
        self.assertTrue((self.tempdir.path / 'foo').is_dir())

    def test_delitem_removes_file(self):
        """Deleting an item removes the corresponding file."""
        self.tempdir.mkfile(path='foo')
        del self.dir['foo']
        self.assertFalse((self.tempdir.path / 'foo').exists())

    def test_delitem_removes_directory(self):
        """Deleting an item removes the corresponding directory."""
        dir_path = self.tempdir.mkdir()
        del self.dir[dir_path.name]
        self.assertFalse(dir_path.exists())

    def test_add(self):
        """Adding two Directory returns joins their path."""
        dir1 = Directory('/foo')
        dir2 = Directory('bar')
        dir = dir1 + dir2
        self.assertEqual(dir.path, Path('/') / 'foo' / 'bar')

    def test_str(self):
        """Covnerting a Directory to a string returns its path."""
        self.assertEqual(str(self.tempdir.path), str(self.dir))
