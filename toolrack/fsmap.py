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

'''Access the filesystem in a dict-like fashion.'''

from os import listdir, mkdir, unlink
from os.path import join, normpath, exists, isfile, isdir
from shutil import rmtree

# Marker for creating directories
DIR = object()


class Directory(object):
    '''Class providing access to the sub-tree of a directrory.'''

    def __init__(self, path):
        self.path = normpath(path)

    def __iter__(self):
        '''Return an iterator yielding names of directory elements.'''
        return iter(listdir(self.path))

    def __getitem__(self, attr):
        '''Access a subitem of the Directory by name.'''
        path = self._get_path(attr)
        if isfile(path):
            with open(path) as fd:
                return fd.read()
        if isdir(path):
            return Directory(path)

    def __setitem__(self, attr, value):
        '''Set the content of a file, or create a sub-directory.'''
        path = join(self.path, attr)
        if value is DIR:
            mkdir(path)
        else:
            with open(path, 'w') as fd:
                fd.write(value)

    def __delitem__(self, attr):
        '''Remove a file or sub-directory.'''
        path = self._get_path(attr)
        if isdir(path):
            rmtree(path)
        else:
            unlink(path)

    def __add__(self, other):
        '''Return a Directory joining paths of two Directories.'''
        return Directory(join(self.path, other.path))

    def _get_path(self, attr):
        '''Return the normalized path for a name.'''
        path = normpath(join(self.path, attr))
        if not exists(path):
            raise KeyError(attr)
        return path
