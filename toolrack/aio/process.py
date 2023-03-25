"""Protocol class for collecting a process stdout/stderr."""

from asyncio import (
    Future,
    get_event_loop,
    SubprocessProtocol,
)
from collections.abc import Callable
from io import StringIO
from typing import cast


class ProcessParserProtocol(SubprocessProtocol):
    """Collect process stdout and stderr.

    If parser functions are be passed for stdout and/or stderr, they are called
    on each full line of output.

    If no parser function is passed, the full output content is returned when
    the process terminates via the ``done`` :class:`Future`.  This returns a
    tuple with the full stdout and stderr. Each tuple element is ``None`` if a
    parser is passed for that stream.

    :param out_parser: an optional parser for the process standard output.
    :param err_parser: an optional parser for the process standard error.

    """

    done: Future

    def __init__(self, out_parser=None, err_parser=None):
        self.done = get_event_loop().create_future()
        self._streams = {
            1: StreamHelper(callback=out_parser),
            2: StreamHelper(callback=err_parser),
        }
        self._data = [None, None]  # hold stdout/stderr data
        self._exception = None
        self._process_exited = False

    def pipe_data_received(self, fd, data):
        stream = self._streams.get(fd)
        if stream:
            stream.receive_data(data.decode())

    def pipe_connection_lost(self, fd, exc):
        stream = self._streams.pop(fd, None)
        if not stream:
            return

        stream.flush_partial()
        self._data[fd - 1] = stream.get_data()
        if exc:
            self._exception = exc
        self._maybe_done()

    def process_exited(self):
        self._process_exited = True
        self._maybe_done()

    def _maybe_done(self):
        if not self._process_exited or self._streams:
            return

        if self._exception:
            self.done.set_exception(self._exception)
        else:
            self.done.set_result(tuple(self._data))


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
        self._buffer = StringIO()
        self._partial = StringIO()

    def receive_data(self, data: str):
        """Receive data and process them.

        If a ``callback`` has been passed to the class, it's called for each
        full line of text.

        """
        if self._callback:
            self._parse_data(data)
        else:
            self._buffer.write(data)

    def get_data(self) -> str | None:
        """Return the full content of the stream if no callback is defined."""
        if self._callback:
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
