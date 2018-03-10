from collections import Iterable

from ..path import match_files
from ..testing import TestCase
from ..testing.fixtures import TempDirFixture


class MatchFilesTests(TestCase):

    def test_return_iterator(self):
        """The method returns an iterator."""
        result = match_files(['dir'], ['match'])
        self.assertIsInstance(result, Iterable)

    def test_multiple_paths(self):
        """The method returns matching files from all provided paths."""
        dir1 = self.useFixture(TempDirFixture())
        dir2 = self.useFixture(TempDirFixture())
        dir1.mkfile(path='name')
        dir2.mkfile(path='name')
        self.assertCountEqual(
            match_files([dir1.path, dir2.path], ['name']),
            [dir1.path / 'name', dir2.path / 'name'])

    def test_glob_match(self):
        """The method returns all files matching the pattern."""
        tempdir = self.useFixture(TempDirFixture())
        tempdir.mkfile(path='name1')
        tempdir.mkfile(path='name2')
        self.assertCountEqual(
            match_files([tempdir.path], ['name*']),
            [tempdir.path / 'name1', tempdir.path / 'name2'])

    def test_multple_matches(self):
        """The method returns files matching all patterns."""
        tempdir = self.useFixture(TempDirFixture())
        tempdir.mkfile(path='this-name')
        tempdir.mkfile(path='other-name')
        tempdir.mkfile(path='name1')
        self.assertCountEqual(
            match_files([tempdir.path], ['name*', '*-name']),
            [tempdir.path / 'this-name', tempdir.path / 'other-name',
             tempdir.path / 'name1'])

    def test_case_sensitive(self):
        """The match is case sensitive by default."""
        tempdir = self.useFixture(TempDirFixture())
        tempdir.mkfile(path='name')
        tempdir.mkfile(path='Name')
        tempdir.mkfile(path='NAME')
        self.assertCountEqual(
            match_files([tempdir.path], ['name']), [tempdir.path / 'name'])

    def test_case_insensitive(self):
        """The match can be made case insensitive."""
        tempdir = self.useFixture(TempDirFixture())
        tempdir.mkfile(path='name')
        tempdir.mkfile(path='Name')
        tempdir.mkfile(path='NAME')
        self.assertCountEqual(
            match_files([tempdir.path], ['name'], ignorecase=True),
            [tempdir.path / 'name', tempdir.path / 'Name',
             tempdir.path / 'NAME'])
