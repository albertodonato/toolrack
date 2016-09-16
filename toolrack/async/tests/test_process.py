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

from textwrap import dedent
from asyncio import Future, new_event_loop, set_event_loop

from ...testing.fixtures import TempDirFixture
from ...testing.async import LoopTestCase
from ..process import ProcessParserProtocol


class ProcessParserProtocolTests(LoopTestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = self.useFixture(TempDirFixture())
        self.future = Future()
        self.protocol_factory = lambda: ProcessParserProtocol(self.future)

    def set_event_loop(self):
        self.loop = new_event_loop()  # use the real event loop
        set_event_loop(self.loop)

    async def test_result(self):
        '''When the process ends, stdout and stderr are returned.'''
        script = dedent(
            '''#!/bin/sh
            echo out
            echo err >&2''')
        cmd = self.tempdir.mkfile(content=script, mode=0o755)

        transport, _ = await self.loop.subprocess_exec(
            self.protocol_factory, cmd)
        self.addCleanup(transport.close)

        result = await self.future
        out, err = result
        self.assertEqual(out, 'out\n')
        self.assertEqual(err, 'err\n')

    async def test_error(self):
        '''If the process errors, an exception is raised.'''
        protocol = ProcessParserProtocol(self.future)
        exception = Exception('fail!')
        # Simulate an error while process is running
        protocol.connection_lost(exception)
        with self.assertRaises(Exception) as e:
            await self.future
        self.assertIs(e.exception, exception)

    async def test_parse_stdout(self):
        '''It's possible to pass a function to parse stdout line by line.'''
        script = dedent(
            '''#!/bin/sh
            echo line 1
            echo not parsed >&2
            echo line 2''')
        cmd = self.tempdir.mkfile(content=script, mode=0o755)

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(
                self.future, out_parser=lines.append)

        transport, _ = await self.loop.subprocess_exec(
            protocol_factory, cmd)
        transport.close()

        await self.future
        self.assertEqual(lines, ['line 1', 'line 2'])

    async def test_parse_stderr(self):
        '''It's possible to pass a function to parse stderr line by line.'''
        script = dedent(
            '''#!/bin/sh
            echo line 1 >&2
            echo not parsed
            echo line 2 >&2''')
        cmd = self.tempdir.mkfile(content=script, mode=0o755)

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(
                self.future, err_parser=lines.append)

        transport, _ = await self.loop.subprocess_exec(
            protocol_factory, cmd)
        transport.close()

        await self.future
        self.assertEqual(lines, ['line 1', 'line 2'])
