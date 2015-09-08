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

from ..property import cachedproperty


class SampleClass:

    def __init__(self, value=True):
        self.value = value
        self.calls = 0

    @cachedproperty
    def property(self):
        self.calls += 1
        return self.value


class CachedpropertyTests(TestCase):

    def test_single_call(self):
        '''The property function is called just once.'''
        obj = SampleClass()
        obj.property
        obj.property
        self.assertEqual(obj.calls, 1)

    def test_value(self):
        '''The property returns the value from the method.'''
        obj = SampleClass(value=100)
        self.assertEqual(obj.property, 100)
