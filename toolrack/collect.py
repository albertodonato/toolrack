"""Collection of objects of the same kind.

A :class:`Collection` holds objects identifying them by the value of an
attribute. For instance::

  collection = Collection('SomeObject', 'name')
  collection.add(obj)

will use ``obj.name`` as key and::

  collection.get('foo')

will return the object with ``obj.name == foo``.

The :class:`Collection` is iterable, and yields the contained objects::

  for obj in collection:
      # ... do something with obj

"""

from collections.abc import Iterator
from typing import Any


class UnknownObject(Exception):
    """No object with the specified key in the :class:`Collection`."""

    def __init__(self, obj_type, obj_key: str):
        super().__init__(f"Unknown {obj_type}: {obj_key}")


class DuplicatedObject(Exception):
    """An object with the specified key is already the :class:`Collection`."""

    def __init__(self, obj_type: type, obj_key: str):
        super().__init__(f"Duplicated {obj_type}: {obj_key}")


class Collection:
    """A Collection of objects keyed on an attribute.

    It collects objects identified by the value of an attribute.
    No objects with duplicated keys are allowed.

    :param obj_type: string identifying the objects type.
    :param key: the object attribute to use as key.

    """

    def __init__(self, obj_type: type, key: str):
        self.obj_type = obj_type
        self.key = key
        self._objects: dict[str, Any] = {}

    def add(self, obj: Any):
        """Add and return an object."""
        key = self._get_key(obj)
        if key in self._objects:
            raise DuplicatedObject(self.obj_type, key)
        self._objects[key] = obj
        return obj

    def get(self, key: str) -> Any:
        """Return the object with the specified key."""
        try:
            return self._objects[key]
        except KeyError:
            raise UnknownObject(self.obj_type, key)

    def remove(self, key: str) -> Any:
        """Remove and return the object with the specified key."""
        obj = self.get(key)
        del self._objects[key]
        return obj

    def keys(self) -> Iterator[str]:
        """Return an iterator with collection keys."""
        return iter(self._objects.keys())

    def sorted(self) -> list:
        """Return a list of objects sorted by key."""
        return sorted(self, key=self._get_key)

    def clear(self):
        """Empty the collection."""
        self._objects.clear()

    def __iter__(self):
        """Return an iterator yielding all objects."""
        return iter(self._objects.values())

    def __contains__(self, key):
        """Whether an object with the specified key is present."""
        return key in self._objects

    def __len__(self):
        """Return the number of objects in the collection."""
        return len(self._objects)

    def _get_key(self, entity):
        """Return the value of the key attribute of the entity."""
        return getattr(entity, self.key)
