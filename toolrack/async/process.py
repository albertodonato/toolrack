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

'''Protocol class for collecting a process stdout/stderr.'''

from io import StringIO
from locale import getpreferredencoding
from asyncio import SubprocessProtocol


class ProcessParserProtocol(SubprocessProtocol):
    '''Collect process stdout and stderr.

    Line parser functions can be passed for stdout and stderr, and they are
    called on each full line of output.  When the process ends, the full output
    and error are returned.

    Parameters:
        - future: an :class:`asyncio.Future` which is called with a tuple with
          (stdout, stderr) from the process once it it exits.
        - out_parser: an optional parser for the process standard output.
        - err_parser: an optional parser for the process standard error.

    '''

    def __init__(self, future, out_parser=None, err_parser=None):
        self.future = future
        self._outputs = {
            fd: _FileDescriptorHelper(parser)
            for fd, parser in enumerate((out_parser, err_parser), 1)}

    def pipe_data_received(self, fd, data):
        stream = self._outputs.get(fd)
        if not stream:
            return

        data = data.decode(getpreferredencoding(False))
        stream.buffer.write(data)
        parser = stream.parser
        if not parser:
            return

        # Append pending partial line
        lines = data.split('\n')
        lines[0] += stream.pop_partial()
        stream.write_partial(lines.pop())
        for line in lines:
            if line:
                parser(line)

    def connection_lost(self, exc):
        stdout = self._outputs[1].buffer.getvalue()
        stderr = self._outputs[2].buffer.getvalue()
        if exc:
            self.future.set_exception(exc)
        else:
            self.future.set_result((stdout, stderr))


class _FileDescriptorHelper:
    '''Helper class to track content for a stream.'''

    def __init__(self, parser):
        self.parser = parser
        self.buffer = StringIO()
        self._partial = StringIO()

    def pop_partial(self):
        '''Return the current partial line and reset it.'''
        line = self._partial.getvalue()
        self._partial.truncate()
        return line

    def write_partial(self, data):
        '''Write a partial line.'''
        self._partial.write(data)
