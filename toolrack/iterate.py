#
# This file is part of ToolRack.
#
# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Utility functions for iterables.'''


def flatten_dict(data, join_char='.', prefix=''):
    '''Flatten a nested dict to (key, value) tuples.

    A neted dict like::

      {'foo': {'bar': 3, 'baz': 4},
       'bza': 'something'}

    is flattened in a sequence of tuples like::

      ('foo.bar': 3), ('foo.baz': 4), ('bza': 'something')


    Parameters:
        - data: a dict to flatten.
        - join_char: the character to use to join key tokens.
        - prefix: an optional prefix to prepend to keys.

    '''
    if isinstance(data, dict):
        base_prefix = prefix
        for key, value in data.items():
            key = str(key)  # force to string
            if base_prefix:
                prefix = join_char.join((base_prefix, key))
            else:
                prefix = key
            yield from flatten_dict(
                value, join_char=join_char, prefix=prefix)

    else:
        yield prefix, data
