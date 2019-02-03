from pathlib import Path

import pytest

from .. import Dir


@pytest.fixture
def dir_path(tmpdir):
    yield Dir(Path(tmpdir))


class TestTempDirFixture:
    def test_join(self, dir_path):
        """join() joins paths under the fixture dir."""
        full_path = dir_path.join("foo", "bar", "baz")
        assert full_path == dir_path.path / "foo" / "bar" / "baz"

    def test_mkdir(self, dir_path):
        """mkdir() creates a directory."""
        path = dir_path.mkdir("foo")
        assert path.is_dir()
        assert path == dir_path.path / "foo"

    def test_mkdir_path_tuple(self, dir_path):
        """mkdir() creates a directory with the path specified as a tuple."""
        path = dir_path.mkdir(("foo", "bar"))
        assert path.is_dir()
        assert path == dir_path.path / "foo" / "bar"

    def test_mkdir_no_absolute_path(self, dir_path):
        """mkdir() raises an error if the path is absolute."""
        with pytest.raises(ValueError) as error:
            dir_path.mkdir("/foo")
        assert str(error.value) == "Path must be relative"

    def test_mkfile(self, dir_path):
        """mkfile() creates a file."""
        path = dir_path.mkfile("foo")
        assert path.is_file()

    def test_mkfile_path_tuple(self, dir_path):
        """mkfile() creates a file with the path specified as a tuple."""
        path = dir_path.mkfile(("foo", "bar"))
        assert path.is_file()
        assert path == dir_path.path / "foo" / "bar"

    def test_mkfile_no_absolute_path(self, dir_path):
        """mkfile() raises an error if the path is absolute."""
        with pytest.raises(ValueError) as error:
            dir_path.mkfile("/foo")
        assert str(error.value) == "Path must be relative"

    def test_mkfile_content(self, dir_path):
        """mkfile() creates a file with specified content."""
        path = dir_path.mkfile("foo", content="some content")
        assert path.read_text() == "some content"

    def test_mkfile_mode(self, dir_path):
        """mkfile() creates a file with specified mode."""
        path = dir_path.mkfile("foo", mode=0o700)
        mode = path.stat().st_mode & 0o777
        assert mode == 0o700

    def test_mksymlink(self, dir_path):
        """mksymlink() creates a symlink to the target."""
        target = dir_path.mkfile()
        link = dir_path.mksymlink(target)
        assert link.parent == dir_path.path
        assert link.is_symlink()

    def test_mksymlink_name(self, dir_path):
        """mksymlink() creates a symlink with specified name."""
        target = dir_path.mkfile()
        link = dir_path.mksymlink(target, path="foo")
        assert link == dir_path.path / "foo"
        assert link.is_symlink()
