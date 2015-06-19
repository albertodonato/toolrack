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

'''Thread-related utilities.'''

from threading import local


class ThreadLocalAttribute:
    '''Descriptor to proxy access to a class attribute, making it thread-local.

    This descriptor can be use to make a class attribute thread-local in a
    trasparent way::

      class MyClass:

          attr = ThreadLocalAttribute('attr')


      instance = MyClass()

    The attribute will be normally accessible as ``instance.attr``, but it's
    stored in a :func:``threading.local`` context.

    '''

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls=None):
        return getattr(self._get_local(obj), self.name)

    def __set__(self, obj, value):
        setattr(self._get_local(obj), self.name, value)

    def __delete__(self, obj):
        delattr(self._get_local(obj), self.name)

    def _get_local(self, obj):
        if not hasattr(obj, '__thread_local'):
            setattr(obj, '__thread_local', local())
        return getattr(obj, '__thread_local')


def thread_local_attrs(*attrs):
    '''Class decorator to make attributes storage thread-local.

    It should be passed names of attributes in the decorated class to make
    local::

      @thread_local_attrs('foo', 'bar')
      class MyClass:

          foo = 3
          bar = None

    '''

    def localize_attrs(cls):
        for attr in attrs:
            setattr(cls, attr, ThreadLocalAttribute(attr))
        return cls

    return localize_attrs
