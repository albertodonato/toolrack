'''Access the filesystem in a dict-like fashion.

This module provides a :class:`Directory` class which provides access to the
filesystem subtree below its path, allow accessing files and sub-directories as
elements of a dict (e.g. ``directory['foo']`` or ``directory['foo/bar']``).

'''

from os import listdir, mkdir, unlink
from os.path import join, normpath, exists, isfile, isdir
from shutil import rmtree

#: Marker for creating directories.
DIR = object()


class Directory:
    '''Provide access to the sub-tree of a directrory.

    It represents a directory in the filesystem::

      directory = Directory('/base/path')

    The object is iterable and yields names of contained elements::

      for elem in directory:
          do_something(directory[elem])

    Sub-directories and files below the base path can be accessed as items of a
    dict. For instance::

      directory['a-dir']['a-file']

    or even with a single access, using OS path format::

      directory['a-dir/a-file']

    Path elements can be removed with ``del``::

      del directory['a-file']
      del directory['a-dir']  # this will delete the whole sub-tree

    Files are created/overwritten by assiging content::

      directory['a-file'] = 'some content'

    and directories are created using the :data:`DIR` marker::

      directory['a-new-dir'] = DIR

    '''

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
