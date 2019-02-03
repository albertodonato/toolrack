from collections.abc import Iterable
from pathlib import Path

from ..path import match_files


class TestMatchFiles:
    def test_return_iterator(self):
        """The method returns an iterator."""
        result = match_files(["dir"], ["match"])
        assert isinstance(result, Iterable)

    def test_multiple_paths(self, tmpdir):
        """The method returns matching files from all provided paths."""
        dir1 = Path(tmpdir / "dir1")
        dir1.mkdir()
        file1 = dir1 / "name"
        file1.touch()
        dir2 = Path(tmpdir / "dir2")
        dir2.mkdir()
        file2 = dir2 / "name"
        file2.touch()
        assert set(match_files([dir1, dir2], ["name"])) == {file1, file2}

    def test_glob_match(self, tmpdir):
        """The method returns all files matching the pattern."""
        file1 = Path(tmpdir / "name1")
        file1.touch()
        file2 = Path(tmpdir / "name2")
        file2.touch()
        assert set(match_files([tmpdir], ["name*"])) == {file1, file2}

    def test_multple_matches(self, tmpdir):
        """The method returns files matching all patterns."""
        file1 = Path(tmpdir / "this-name")
        file1.touch()
        file2 = Path(tmpdir / "other-name")
        file2.touch()
        file3 = Path(tmpdir / "name1")
        file3.touch()
        assert set(match_files([tmpdir], ["name*", "*-name"])) == {file1, file2, file3}

    def test_case_sensitive(self, tmpdir):
        """The match is case sensitive by default."""
        file1 = Path(tmpdir / "name")
        file1.touch()
        file2 = Path(tmpdir / "Name")
        file2.touch()
        file3 = Path(tmpdir / "NAME")
        file3.touch()
        assert set(match_files([tmpdir], ["name"])) == {file1}

    def test_case_insensitive(self, tmpdir):
        """The match can be made case insensitive."""
        file1 = Path(tmpdir / "name")
        file1.touch()
        file2 = Path(tmpdir / "Name")
        file2.touch()
        file3 = Path(tmpdir / "NAME")
        file3.touch()
        assert set(match_files([tmpdir], ["name"], ignorecase=True)) == {
            file1,
            file2,
            file3,
        }
