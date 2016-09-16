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

    , and return it with a :class:`asyncio.Future'.
    '''

    def __init__(self, future, out_parser=None, err_parser=None):
        self.future = future
        self._outputs = {
            fd: {'buffer': StringIO(),
                 'partial': '',
                 'parser': parser}
            for fd, parser in enumerate((out_parser, err_parser), 1)}

    def pipe_data_received(self, fd, data):
        output = self._outputs.get(fd)
        if not output:
            return

        data = data.decode(getpreferredencoding(False))
        output['buffer'].write(data)
        parser = output['parser']
        if not parser:
            return

        # Append pending partial output
        lines = data.split('\n')
        lines[0] = output['partial'] + lines[0]
        output['partial'] = lines.pop()
        for line in lines:
            if line:
                parser(line)

    def connection_lost(self, exc):
        stdout = self._outputs[1]['buffer'].getvalue()
        stderr = self._outputs[2]['buffer'].getvalue()
        if exc:
            self.future.set_exception(exc)
        else:
            self.future.set_result((stdout, stderr))
