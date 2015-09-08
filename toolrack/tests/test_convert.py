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

from unittest import TestCase

from ..convert import convert_bbyte


class ConvertBbyteTests(TestCase):

    def test_convert_no_conversion(self):
        '''If no from/to multipliers are provided, no conversion is made.'''
        self.assertEqual(convert_bbyte(1024), 1024)

    def test_convert_form(self):
        '''It's possible to convert form a multiplier to bytes.'''
        self.assertEqual(convert_bbyte(1, suffix='kib'), 1024)
        self.assertEqual(convert_bbyte(1, suffix='mib'), 1048576)

    def test_convert_to(self):
        '''It's possible to convert to a multiplier from bytes.'''
        self.assertEqual(convert_bbyte(1073741824, to='gib'), 1)
        self.assertEqual(convert_bbyte(1099511627776, to='tib'), 1)

    def test_convert_from_to(self):
        '''It's possible to covert across multipliers.'''
        self.assertEqual(convert_bbyte(1024, suffix='mib', to='gib'), 1)
        self.assertEqual(convert_bbyte(1048576, suffix='kib', to='gib'), 1)
