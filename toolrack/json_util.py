"""Utilities for dealing with JSON data."""

from json import (
    dump,
    load,
)


def indent(in_fd, out_fd, indent=4, ensure_ascii=False):
    """Indent JSON data.

    It reads text in JSON format from ``in_fd`` and writes the formatted output
    to ``out_fd``, using the specified amount of ``indent`` spaces.

    :param in_fd: input file descriptor.
    :param out_fd: output file descriptor.
    :param int indent: number of spaces used for indentation.
    :param bool ensure_ascii: passed to the JSON serializer, if specified,
        non-ASCII characters are escaped.

    """
    data = load(in_fd)
    dump(data, out_fd, sort_keys=True, ensure_ascii=ensure_ascii, indent=indent)
    out_fd.write("\n")
