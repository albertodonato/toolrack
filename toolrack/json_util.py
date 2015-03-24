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

'''Utilities for dealing with JSON data.'''

from json import load, dump


def indent(in_fd, out_fd, indent=4, ensure_ascii=False):
    '''Indent JSON data.

    It reads text in JSON format from ``in_fd`` and writes the formatted output
    to ``out_fd``, using the specified amount of ``indent`` spaces.

    Parameters:
        - in_fd: input file descriptor.
        - out_fd: output file descriptor.
        - indent: number of spaces used for indentation.
        - ensure_ascii: passed to the JSON serializer, if specified, non-ASCII
          characters are escaped.

    '''
    data = load(in_fd)
    dump(
        data, out_fd, sort_keys=True, ensure_ascii=ensure_ascii,
        indent=indent)
    out_fd.write('\n')
