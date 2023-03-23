"""Protocol class for collecting a process stdout/stderr."""

from asyncio import (
    Future,
    SubprocessProtocol,
)
from collections.abc import Callable
from io import StringIO
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

    :param future: a Future called with a tuple with (stdout, stderr) from the
        process once it it exits.
    :param out_parser: an optional parser for the process standard output.
    :param err_parser: an optional parser for the process standard error.

    """

    def __init__(self, future: Future, out_parser=None, err_parser=None):
        self.future = future
        self._outputs = {
            fd: StreamHelper(callback=parser)
            for fd, parser in enumerate((out_parser, err_parser), 1)
        }
        self._exception = None
        self._data = ["", ""]  # hold stdout/stderr data

    def pipe_data_received(self, fd, data):
        stream = self._outputs[fd]
        stream.receive_data(data.decode())

    def pipe_connection_lost(self, fd, exc):
        output = self._outputs.get(fd)
        if not output:
            return
        output.flush_partial()
        if exc:
            self._exception = exc
            return
        self._data[fd - 1] = output.get_data()

    def process_exited(self):
        if self._exception:
            self.future.set_exception(self._exception)
        else:
            self.future.set_result(tuple(self._data))


class StreamHelper:
    """Helper to cache data until full lines of text are received.

    This is useful to collect data from a stream and process them when full
    lines are received.
    For example::

      stream = StreamHelper(callback=callback)
      stream.receive_data('line one\\nline two')
      stream.receive_data('continues here\\n')

    would call ``callback`` twice, one with ``'line one'`` and one with
    ``'line two continues here'``

    :param callable callback: an optional function which is called with full
        lines of text from the stream.
    :param str separator: the line separator

    """

    def __init__(
        self,
        callback: Callable[[str], None] | None = None,
        separator: str = "\n",
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

    def get_data(self) -> str | None:
        """Return the full content of the stream if no callback is defined."""
        if not self._buffer:
            return None
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
        if not data:
            return
        lines = data.split(self.separator)
        if len(lines) > 1:  # at least one full line
            lines[0] = self._pop_partial() + lines[0]
        # might be empty if data ended with separator
        self._partial.write(lines.pop())
        # call the callback on full lines
        for line in lines:
            cast(Callable, self._callback)(line)

    def _pop_partial(self):
        """Return the current partial line and reset it."""
        line = self._partial.getvalue()
        self._partial.truncate(0)
        return line
