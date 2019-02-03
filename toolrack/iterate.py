"""Utility functions for iterables."""


def flatten_dict(data, join_char=".", prefix=""):
    """Flatten a nested dict to (key, value) tuples.

    A neted dict like::

      {'foo': {'bar': 3, 'baz': 4},
       'bza': 'something'}

    is flattened in a sequence of tuples like::

      ('foo.bar': 3), ('foo.baz': 4), ('bza': 'something')


    :param dict data: a dict to flatten.
    :param str join_char: the character to use to join key tokens.
    :param str prefix: an optional prefix to prepend to keys.

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
