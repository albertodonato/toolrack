from unittest import TestCase

from ..iterate import flatten_dict


class FlattenDictTests(TestCase):

    def test_flatten_flat_dict(self):
        """when passed a flat dict, flatten_dict return key, value pairs."""
        items = flatten_dict({'a': 3, 'b': 4})
        self.assertCountEqual(items, [('a', 3), ('b', 4)])

    def test_flatten_dict_of_dict(self):
        """If passed a dict of dict, flatten_dict flatten keys."""
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data)
        self.assertCountEqual(items, [('a.1', 1), ('b.2', 2)])

    def test_flatten_dict_mixed(self):
        """Keys for midex-type dicts are flattened."""
        data = {'a': {'1': 1}, 'b': 2}
        items = flatten_dict(data)
        self.assertCountEqual(items, [('a.1', 1), ('b', 2)])

    def test_flatten_dict_mixed_multi_level(self):
        """Keys for midex-type dicts are flattened at different levels."""
        data = {
            'a': {'1': 1, '3': {'9': 'foo'}},
            'b': {'2': {'x': 9}, 'bar': 'baz'}}
        items = flatten_dict(data)
        self.assertCountEqual(
            items,
            [('a.1', 1), ('a.3.9', 'foo'), ('b.2.x', 9), ('b.bar', 'baz')])

    def test_flatten_dict_join_char(self):
        """A custom join_char can be specified."""
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data, join_char='-')
        self.assertCountEqual(items, [('a-1', 1), ('b-2', 2)])

    def test_flatten_dict_prefix(self):
        """A prefix can be specified."""
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data, prefix='pre')
        self.assertCountEqual(items, [('pre.a.1', 1), ('pre.b.2', 2)])

    def test_flatten_dict_key_not_string(self):
        """If the key is not a string, it's converted to string."""
        items = flatten_dict({1: 'a'})
        self.assertCountEqual(items, [('1', 'a')])
