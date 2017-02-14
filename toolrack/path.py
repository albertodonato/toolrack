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
