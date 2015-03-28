#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Utilities for unit conversion.'''


#: Binary byte multipliers
BYTE_SUFFIXES = (None, 'kib', 'mib', 'gib', 'tib', 'pib', 'eib', 'zib', 'yib')


def convert_bbyte(value, suffix=None, to=None):
    '''Convert a binary byte value across multipliers.

    Parameters:
        - value: the current value.
        - suffix: the current multiplier for the value (`None` for bytes).
        - to: the target multiplier (`None` for bytes).

    '''
    if suffix:
        suffix = suffix.lower()
    multiplier = 2 ** (10 * BYTE_SUFFIXES.index(suffix))
    converted = value * multiplier
    if to:
        to = to.lower()
        divider = 2 ** (10 * BYTE_SUFFIXES.index(to))
        converted = converted / divider
    return converted
