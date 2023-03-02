"""Protocol class for collecting a process stdout/stderr."""

from asyncio import (
    Future,
    SubprocessProtocol,
)
from collections.abc import Callable
from io import StringIO
from locale import getpreferredencoding
from typing import (
    cast,
    IO,
)


class ProcessParserProtocol(SubprocessProtocol):
    """Collect process stdout and stderr.

    Line parser functions can be passed for stdout and stderr, and they are
    called on each full line of output.

    When the process ends, the ``future`` returns a tuple with the full stdout
    and stderr. Each tuple element is ``None`` if a parser is passed for that
    stream.

    :param asyncio.Future future: a Future called with a tuple with
        (stdout, stderr) from the process once it it exits.
    :param callable out_parser: an optional parser for the process standard
        output.
    :param callable err_parser: an optional parser for the process standard
        error.

    """

    def __init__(self, future: Future, out_parser=None, err_parser=None):
        self.future = future
        self._outputs = {
            fd: StreamHelper(callback=parser)
            for fd, parser in enumerate((out_parser, err_parser), 1)
        }

    def pipe_data_received(self, fd, data):
        stream = self._outputs[fd]
        data = data.decode(getpreferredencoding(False))
        stream.receive_data(data)

    def connection_lost(self, exc):
        self._outputs[1].flush_partial()
        self._outputs[2].flush_partial()
        stdout = self._outputs[1].get_data()
        stderr = self._outputs[2].get_data()
        if exc:
            self.future.set_exception(exc)
        else:
            self.future.set_result((stdout, stderr))


class StreamHelper:
    """Helper to cache data until full lines of text are received.

    This is useful to collect data from a stream and process them when full
    lines are received.
    For example::

      stream = StreamHelper(callback)
      stream.receive_data('line one\\nline two')
      stream.receive_data('continues here\\n')

    would call ``callback`` twice, one with ``'line one'`` and one with
    ``'line two continues here'``

    :param callable callback: an optional function which is called with full
        lines of text from the stream.
    :param str separator: the line separator

    """

    def __init__(
        self, callback: Callable[[str], None] | None = None, separator: str = "\n"
    ):
        self.separator = separator
        self._callback = callback
        self._buffer = StringIO() if not callback else None
        self._partial = StringIO()

    def receive_data(self, data: str):
        """Receive data and process them.

        If a ``callback`` has been passed to the class, it's called for each
        full line of text.

        """
        if self._callback:
            self._parse_data(data)
        else:
            cast(IO, self._buffer).write(data)

    def get_data(self):
        """Return the full content of the stream."""
        if not self._buffer:
            return
        return self._buffer.getvalue() + self._partial.getvalue()

    def flush_partial(self):
        """Flush and process pending data from a partial line."""
        if not self._callback:
            return
        partial = self._partial.getvalue()
        if partial:
            self._callback(partial)

    def _parse_data(self, data: str):
        """Process data parsing full lines."""
        lines = data.split(self.separator)
        lines[0] = self._pop_partial() + lines[0]
        self._partial.write(lines.pop())
        # Call the callback on full lines
        for line in lines:
            if line:
                cast(Callable, self._callback)(line)

    def _pop_partial(self):
        """Return the current partial line and reset it."""
        line = self._partial.getvalue()
        self._partial.truncate()
        return line
