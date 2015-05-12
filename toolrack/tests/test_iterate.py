#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from toolrack.iterate import flatten_dict


class FlattenDictTests(TestCase):

    def test_flatten_flat_dict(self):
        '''when passed a flat dict, flatten_dict return key, value pairs.'''
        items = flatten_dict({'a': 3, 'b': 4})
        self.assertCountEqual(items, [('a', 3), ('b', 4)])

    def test_flatten_dict_of_dict(self):
        '''If passed a dict of dict, flatten_dict flatten keys.'''
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data)
        self.assertCountEqual(items, [('a.1', 1), ('b.2', 2)])

    def test_flatten_dict_mixed(self):
        '''Keys for midex-type dicts are flattened.'''
        data = {'a': {'1': 1}, 'b': 2}
        items = flatten_dict(data)
        self.assertCountEqual(items, [('a.1', 1), ('b', 2)])

    def test_flatten_dict_mixed_multi_level(self):
        '''Keys for midex-type dicts are flattened at different levels.'''
        data = {
            'a': {'1': 1, '3': {'9': 'foo'}},
            'b': {'2': {'x': 9}, 'bar': 'baz'}}
        items = flatten_dict(data)
        self.assertCountEqual(
            items,
            [('a.1', 1), ('a.3.9', 'foo'), ('b.2.x', 9), ('b.bar', 'baz')])

    def test_flatten_dict_join_char(self):
        '''A custom join_char can be specified.'''
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data, join_char='-')
        self.assertCountEqual(items, [('a-1', 1), ('b-2', 2)])

    def test_flatten_dict_prefix(self):
        '''A prefix can be specified.'''
        data = {'a': {'1': 1}, 'b': {'2': 2}}
        items = flatten_dict(data, prefix='pre')
        self.assertCountEqual(items, [('pre.a.1', 1), ('pre.b.2', 2)])

    def test_flatten_dict_key_not_string(self):
        '''If the key is not a string, it's converted to string.'''
        items = flatten_dict({1: 'a'})
        self.assertCountEqual(items, [('1', 'a')])
