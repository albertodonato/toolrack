from collections import Counter

import pytest

from ..collect import (
    Collection,
    DuplicatedObject,
    UnknownObject,
)


class SampleObject:
    def __init__(self, name, other_attr=None):
        self.name = name
        self.other_attr = other_attr


@pytest.fixture
def collection():
    yield Collection("SampleObject", "name")


class TestCollection:
    def test_add(self, collection):
        """Objects can be added to the Collection."""
        obj = SampleObject("foo")
        returned = collection.add(obj)
        assert returned is obj
        assert collection.get("foo") is obj

    def test_add_duplicated(self, collection):
        """An error is raised if the object key is already present."""
        obj1 = SampleObject("foo")
        obj2 = SampleObject("foo")
        collection.add(obj1)
        with pytest.raises(DuplicatedObject):
            collection.add(obj2)

    def test_in_present(self, collection):
        """The key is present in the Collection."""
        collection.add(SampleObject("foo"))
        assert "foo" in collection

    def test_in_absent(self, collection):
        """The key is not present in the Collection."""
        assert "foo" not in collection

    def test_custom_key(self):
        """It's possible to use a different attribute as key."""
        collection = Collection("Object", key="other_attr")
        obj = SampleObject("foo", other_attr="bar")
        collection.add(obj)
        assert collection.get("bar") is obj

    def test_remove(self, collection):
        """Objects can be removed from the Collection."""
        obj = SampleObject("foo")
        collection.add(obj)
        returned = collection.remove("foo")
        assert returned is obj
        with pytest.raises(UnknownObject):
            collection.remove("foo")

    def test_remove_unknown(self, collection):
        """An error is raised if the object key is unknown."""
        with pytest.raises(UnknownObject):
            collection.remove("foo")

    def test_iterable(self, collection):
        """The Collection is iterable."""
        objs = [SampleObject("foo"), SampleObject("bar"), SampleObject("baz")]
        for obj in objs:
            collection.add(obj)
        assert Counter(collection) == Counter(objs)

    def test_keys(self, collection):
        """The Collection returns an iterable with keys."""
        objs = [SampleObject("foo"), SampleObject("bar"), SampleObject("baz")]
        for obj in objs:
            collection.add(obj)
        assert list(collection.keys()) == ["foo", "bar", "baz"]

    def test_len(self, collection):
        """The length of a Collection is the number of objects in it."""
        collection.add(SampleObject("foo"))
        collection.add(SampleObject("bar"))
        assert len(collection) == 2

    def test_sorted(self, collection):
        """The Collection can return objects ordered by key."""
        objs = [SampleObject("bar"), SampleObject("baz"), SampleObject("foo")]
        # Add objects in a different order.
        collection.add(objs[1])
        collection.add(objs[0])
        collection.add(objs[2])
        assert collection.sorted() == objs

    def test_clear(self, collection):
        """The Collection can be cleared."""
        collection.add(SampleObject("foo"))
        collection.add(SampleObject("bar"))
        collection.clear()
        assert len(collection) == 0
