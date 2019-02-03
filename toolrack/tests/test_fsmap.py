from os import path
from pathlib import Path

import pytest

from ..fsmap import (
    DIR,
    Directory,
)


@pytest.fixture
def directory(tempdir):
    yield Directory(tempdir.path)


class TestDirectory:
    def test_iter_list_files(self, tempdir, directory):
        """Iterating on the Directory returns contained file names."""
        tempdir.mkfile(path="foo")
        tempdir.mkfile(path="bar")
        assert sorted(directory) == [tempdir / "bar", tempdir / "foo"]

    def test_getitem_reads_file(self, tempdir, directory):
        """Accessing a file item returns the content."""
        tempdir.mkfile(path="foo", content="some foo")
        assert directory["foo"] == "some foo"

    def test_getitem_returns_directory(self, tempdir, directory):
        """Accessing a file item returns the content."""
        dir_path = tempdir.mkdir()
        assert isinstance(directory[dir_path.name], Directory)

    def test_getitem_traverses_paths(self, tempdir, directory):
        """It's possible to traverse subdirectories when accessing elements."""
        file_path = path.join("subdir", "file")
        tempdir.mkfile(path=file_path, content="some content")
        assert directory[file_path] == "some content"

    def test_getitem_notfound_raises(self, directory):
        """An error is raised if the element is not found."""
        with pytest.raises(KeyError):
            directory["unknown"]

    def test_setitem_writes_file(self, tempdir, directory):
        """Setting an element writes the file."""
        directory["foo"] = "some content"
        assert (tempdir / "foo").read_text() == "some content"

    def test_setitem_creates_directory(self, tempdir, directory):
        """Setting an item to DIR creates the directory."""
        directory["foo"] = DIR
        assert (tempdir / "foo").is_dir()

    def test_delitem_removes_file(self, tempdir, directory):
        """Deleting an item removes the corresponding file."""
        tempdir.mkfile(path="foo")
        del directory["foo"]
        assert not (tempdir / "foo").exists()

    def test_delitem_removes_directory(self, tempdir, directory):
        """Deleting an item removes the corresponding directory."""
        dir_path = tempdir.mkdir()
        del directory[dir_path.name]
        assert not dir_path.exists()

    def test_add(self):
        """Adding two Directory returns joins their path."""
        dir1 = Directory("/foo")
        dir2 = Directory("bar")
        directory = dir1 + dir2
        assert directory.path == Path("/") / "foo" / "bar"

    def test_str(self, tempdir, directory):
        """Covnerting a Directory to a string returns its path."""
        assert str(tempdir) == str(directory)
