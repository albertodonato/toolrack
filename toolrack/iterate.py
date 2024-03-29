"""Utility functions for iterables."""

from collections.abc import Iterator
from typing import (
    Any,
)


def flatten_dict(
    data: Any, join_char: str = ".", prefix: str = ""
) -> Iterator[tuple[str, Any]]:
    """Flatten a nested dict to `(key, value)` tuples.

    A nested dict like::

      {'foo': {'bar': 3, 'baz': 4},
       'bza': 'something'}

    is flattened in a sequence of tuples like::

      ('foo.bar': 3), ('foo.baz': 4), ('bza': 'something')


    :param data: a dict to flatten.
    :param join_char: the character to use to join key tokens.
    :param prefix: an optional prefix to prepend to keys.

    """
    if isinstance(data, dict):
        base_prefix = prefix
        for key, value in data.items():
            key = str(key)  # force to string
            if base_prefix:
                prefix = join_char.join((base_prefix, key))
            else:
                prefix = key
            yield from flatten_dict(value, join_char=join_char, prefix=prefix)

    else:
        yield prefix, data
