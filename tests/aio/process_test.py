from asyncio import Future
from pathlib import Path
from textwrap import dedent

import pytest

from toolrack.aio.process import (
    ProcessParserProtocol,
    StreamHelper,
)


@pytest.fixture
def future(event_loop):
    yield Future(loop=event_loop)


@pytest.fixture
def protocol_factory(future):
    yield lambda: ProcessParserProtocol(future)


@pytest.fixture
def executable(tmpdir):
    executable = Path(tmpdir / "exe")
    executable.touch()
    executable.chmod(0o755)
    yield executable


@pytest.fixture
def write_executable(executable):
    yield lambda content: executable.write_text(content)


@pytest.fixture
def exec_process(event_loop, future, protocol_factory, executable):
    async def run():
        transport, _ = await event_loop.subprocess_exec(
            protocol_factory, str(executable)
        )
        result = await future
        transport.close()
        return result

    return run


@pytest.mark.asyncio
class TestProcessParserProtocol:
    async def test_result(self, exec_process, write_executable):
        """When the process ends, stdout and stderr are returned."""
        write_executable(
            dedent(
                """#!/bin/sh
                echo out
                echo err >&2
                """
            )
        )

        result = await exec_process()
        out, err = result
        assert out == "out\n"
        assert err == "err\n"

    async def test_error(self, future):
        """If the process errors, an exception is raised."""
        protocol = ProcessParserProtocol(future)
        exception = Exception("fail!")
        # Simulate an error while process is running
        protocol.pipe_connection_lost(1, exception)
        protocol.process_exited()
        with pytest.raises(Exception) as error:
            await future
        assert error.value is exception

    @pytest.mark.asyncio
    async def test_parse_stdout(
        self, event_loop, future, executable, exec_process, write_executable
    ):
        """It's possible to pass a function to parse stdout line by line."""
        write_executable(
            dedent(
                """#!/bin/sh
                echo line 1
                echo not parsed >&2
                echo line 2
                """
            )
        )

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(future, out_parser=lines.append)

        transport, _ = await event_loop.subprocess_exec(
            protocol_factory, str(executable)
        )
        transport.close()

        result = await future
        assert lines == ["line 1", "line 2"]
        # Full stdout is not returned
        assert result == (None, "not parsed\n")

    @pytest.mark.asyncio
    async def test_parse_stderr(
        self, event_loop, future, executable, write_executable
    ):
        """It's possible to pass a function to parse stderr line by line."""
        write_executable(
            dedent(
                """#!/bin/sh
                echo line 1 >&2
                echo not parsed
                echo line 2 >&2
                """
            )
        )

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(future, err_parser=lines.append)

        transport, _ = await event_loop.subprocess_exec(
            protocol_factory, str(executable)
        )
        transport.close()

        result = await future
        assert lines == ["line 1", "line 2"]
        # Full stderr is not returned
        assert result == ("not parsed\n", None)

    async def test_parse_no_ending_newline(
        self, event_loop, future, executable, write_executable
    ):
        """The last line of output is partse if it doesn't have a newline."""
        write_executable(
            dedent(
                """#!/bin/sh
                echo line 1
                echo -n line 2
                """
            )
        )

        lines = []

        def protocol_factory():
            return ProcessParserProtocol(future, out_parser=lines.append)

        transport, _ = await event_loop.subprocess_exec(
            protocol_factory, str(executable)
        )
        transport.close()

        await future
        assert lines == ["line 1", "line 2"]


class TestStreamHelper:
    @pytest.mark.parametrize(
        "data,lines",
        [
            (("foo\n", "bar\n", "baz\n"), ["foo", "bar", "baz"]),
            (("foo\nbar", "baz\n"), ["foo", "barbaz"]),
            (("foo\n", "bar\n", "baz"), ["foo", "bar", "baz"]),
        ],
    )
    def test_with_callback(self, data, lines):
        """The callback is called with full lines of data."""
        callback_lines = []
        helper = StreamHelper(callback=callback_lines.append)
        for part in data:
            helper.receive_data(part)
        helper.flush_partial()
        assert callback_lines == lines

    @pytest.mark.parametrize(
        "data,output",
        [
            (("foo\n", "bar\n", "baz\n"), "foo\nbar\nbaz\n"),
            (("foo\nbar", "baz\n"), "foo\nbarbaz\n"),
            (("foo\n", "bar\n", "baz"), "foo\nbar\nbaz"),
        ],
    )
    def test_no_callbacks(self, data, output):
        helper = StreamHelper()
        for part in data:
            helper.receive_data(part)
        assert helper.get_data() == output

    def test_receive_data_separator(self):
        """It's possible to specify a different line separator."""
        lines = []
        helper = StreamHelper(callback=lines.append, separator="X")
        helper.receive_data("fooXbarX")
        assert lines == ["foo", "bar"]
