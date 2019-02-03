"""Functions for paths handling."""

from fnmatch import fnmatch
from os import walk
from pathlib import Path


def match_files(dirpaths, patterns, ignorecase=False):
    """Search files by name based on shell patterns.

    :param list dirpaths: a list of paths to search from.
    :param list patterns: a list of name patterns to match.

    :returns: an iterator yielding matched files.

    """
    for dirpath in dirpaths:
        for dirname, _, filenames in walk(str(dirpath)):
            for filename in filenames:
                fname = filename.lower() if ignorecase else filename
                if any(fnmatch(fname, pattern) for pattern in patterns):
                    yield Path(dirname) / filename
