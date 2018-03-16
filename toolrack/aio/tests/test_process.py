from asyncio import Future
from textwrap import dedent
from unittest import TestCase

from asynctest import TestCase as AsyncTestCase
from fixtures import TestWithFixtures

from ..process import (
    ProcessParserProtocol,
    StreamHelper,
)
from ...testing.fixtures import TempDirFixture


class ProcessParserProtocolTests(TestWithFixtures, AsyncTestCase):

    def setUp(self):
        super().setUp()
        self.tempdir = self.useFixture(TempDirFixture())
        self.future = Future()
        self.protocol_factory = lambda: ProcessParserProtocol(self.future)

    def make_command(self, content):
        """create a test script and return its path."""
        return str(self.tempdir.mkfile(content=content, mode=0o755))

    async def test_result(self):
        """When the process ends, stdout and stderr are returned."""
        script = dedent(
            '''#!/bin/sh
            echo out
            echo err >&2''')
        cmd = self.make_command(script)

        transport, _ = await self.loop.subprocess_exec(
            self.protocol_factory, cmd)
        self.addCleanup(transport.close)

        result = await self.future
        out, err = result
        self.assertEqual(out, 'out\n')
        self.assertEqual(err, 'err\n')

    async def test_error(self):
        """If the process errors, an exception is raised."""
        protocol = ProcessParserProtocol(self.future)
        exception = Exception('fail!')
        # Simulate an error while process is running
        protocol.connection_lost(exception)
        with self.assertRaises(Exception) as e:
            await self.future
        self.assertIs(e.exception, exception)

    async def test_parse_stdout(self):
        """It's possible to pass a function to parse stdout line by line."""
        script = dedent(
            '''#!/bin/sh
            echo line 1
            echo not parsed >&2
            echo line 2''')
        cmd = self.make_command(script)

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(
                self.future, out_parser=lines.append)

        transport, _ = await self.loop.subprocess_exec(
            protocol_factory, cmd)
        transport.close()

        result = await self.future
        self.assertEqual(lines, ['line 1', 'line 2'])
        # Full stdout is not returned
        self.assertEqual(result, (None, 'not parsed\n'))

    async def test_parse_stderr(self):
        """It's possible to pass a function to parse stderr line by line."""
        script = dedent(
            '''#!/bin/sh
            echo line 1 >&2
            echo not parsed
            echo line 2 >&2''')
        cmd = self.make_command(script)

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(
                self.future, err_parser=lines.append)

        transport, _ = await self.loop.subprocess_exec(
            protocol_factory, cmd)
        transport.close()

        result = await self.future
        self.assertEqual(lines, ['line 1', 'line 2'])
        # Full stderr is not returned
        self.assertEqual(result, ('not parsed\n', None))

    async def test_parse_no_ending_newline(self):
        """The last line of output is partse if it doesn't have a newline."""
        script = dedent(
            '''#!/bin/sh
            echo line 1
            echo -n line 2''')
        cmd = self.make_command(script)

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(
                self.future, out_parser=lines.append)

        transport, _ = await self.loop.subprocess_exec(
            protocol_factory, cmd)
        transport.close()

        await self.future
        self.assertEqual(lines, ['line 1', 'line 2'])


class StreamHelperTests(TestCase):

    def setUp(self):
        super().setUp()
        self.lines = []

    def test_receive_data_handles_partial(self):
        """receive_data caches partial lines and joins them. """
        helper = StreamHelper(callback=self.lines.append)
        helper.receive_data('foo\nbar')
        self.assertEqual(self.lines, ['foo'])
        helper.receive_data('baz\n')
        self.assertEqual(self.lines, ['foo', 'barbaz'])

    def test_receive_data_separator(self):
        """It's possible to specify a different line separator. """
        helper = StreamHelper(callback=self.lines.append, separator='X')
        helper.receive_data('fooXbarX')
        self.assertEqual(self.lines, ['foo', 'bar'])
