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

'''Functions for paths handling.'''

from os import walk
from fnmatch import fnmatch


def match_files(dirpaths, patterns, ignorecase=False):
    '''Search files by name based on shell patterns.

    A list of paths to search in and patters to match can be provided.

    An iterator yielding tuples with directory and file name for each match is
    returned.

    '''
    for dirpath in dirpaths:
        for dirname, _, filenames in walk(dirpath):
            for filename in filenames:
                fname = filename.lower() if ignorecase else filename
                if any(fnmatch(fname, pattern) for pattern in patterns):
                    yield dirname, filename
