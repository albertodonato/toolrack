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

'''Property decorators.'''


class cachedproperty:
    '''Decorator to a class method a cached property.

    The property method is called just the first time for an instance, and its
    result cached.

    '''

    def __init__(self, func):
        self._func = func
        self._name = func.__name__

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        value = self._func(obj)
        # The property itself is replaced with the result of the function call
        setattr(obj, self._name, value)
        return value