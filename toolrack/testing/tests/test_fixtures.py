import os

from .. import TestCase
from ..fixtures import TempDirFixture


class TempDirFixtureTests(TestCase):

    def setUp(self):
        super().setUp()
        self.fixture = self.useFixture(TempDirFixture())

    def test_join(self):
        '''join() joins paths under the fixture dir.'''
        full_path = self.fixture.join('foo', 'bar', 'baz')
        self.assertEqual(
            os.path.join(self.fixture.path, 'foo', 'bar', 'baz'), full_path)

    def test_mkdir(self):
        '''mkdir() creates a directory.'''
        dir_path = os.path.join(self.fixture.path, 'foo')
        self.fixture.mkdir('foo')
        self.assertTrue(os.path.isdir(dir_path))

    def test_mkdir_path_tuple(self):
        '''mkdir() creates a directory with the path specified as a tuple.'''
        dir_path = os.path.join(self.fixture.path, 'foo', 'bar')
        self.fixture.mkdir(('foo', 'bar'))
        self.assertTrue(os.path.isdir(dir_path))

    def test_mkdir_no_absolute_path(self):
        '''mkdir() raises an error if the path is absolute.'''
        with self.assertRaises(ValueError) as cm:
            self.fixture.mkdir('/foo')
        self.assertEqual(str(cm.exception), 'Path must be relative')

    def test_mkfile(self):
        '''mkfile() creates a file.'''
        file_path = os.path.join(self.fixture.path, 'foo')
        self.fixture.mkfile('foo')
        self.assertTrue(os.path.isfile(file_path))

    def test_mkfile_path_tuple(self):
        '''mkfile() creates a file with the path specified as a tuple.'''
        file_path = os.path.join(self.fixture.path, 'foo', 'bar')
        self.fixture.mkfile(('foo', 'bar'))
        self.assertTrue(os.path.isfile(file_path))

    def test_mkfile_no_absolute_path(self):
        '''mkfile() raises an error if the path is absolute.'''
        with self.assertRaises(ValueError) as cm:
            self.fixture.mkfile('/foo')
        self.assertEqual(str(cm.exception), 'Path must be relative')

    def test_mkfile_content(self):
        '''mkfile() creates a file with specified content.'''
        file_path = os.path.join(self.fixture.path, 'foo')
        self.fixture.mkfile('foo', content='some content')
        self.assertEqual(self.readfile(file_path), 'some content')

    def test_mkfile_mode(self):
        '''mkfile() creates a file with specified mode.'''
        file_path = os.path.join(self.fixture.path, 'foo')
        self.fixture.mkfile('foo', mode=0o700)
        mode = os.stat(file_path).st_mode & 0o777
        self.assertEqual(mode, 0o700)
