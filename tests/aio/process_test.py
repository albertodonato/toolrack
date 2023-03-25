from pathlib import Path
from textwrap import dedent

import pytest

from toolrack.aio.process import (
    ProcessParserProtocol,
    StreamHelper,
)


@pytest.fixture
def executable(tmpdir):
    executable = Path(tmpdir / "exe")
    executable.touch()
    executable.chmod(0o755)
    yield executable


@pytest.fixture
def exec_process(event_loop, executable):
    async def run(protocol_factory=ProcessParserProtocol):
        transport, protocol = await event_loop.subprocess_exec(
            protocol_factory, str(executable)
        )
        result = await protocol.done
        transport.close()
        return result

    return run


@pytest.mark.asyncio
class TestProcessParserProtocol:
    async def test_result(self, executable, exec_process):
        """When the process ends, stdout and stderr are returned."""
        executable.write_text(
            dedent(
                """#!/bin/sh
                echo out
                echo err >&2
                """
            )
        )

        out, err = await exec_process()
        assert out == "out\n"
        assert err == "err\n"

    async def test_error(self, event_loop):
        """If the process errors, an exception is raised."""
        protocol = ProcessParserProtocol()
        exception = Exception("fail!")
        # Simulate an error while process is running
        protocol.pipe_connection_lost(1, exception)
        protocol.pipe_connection_lost(2, None)
        protocol.process_exited()
        with pytest.raises(Exception) as error:
            await protocol.done
        assert error.value is exception

    @pytest.mark.asyncio
    async def test_parse_stdout(self, event_loop, executable, exec_process):
        """It's possible to pass a function to parse stdout line by line."""
        executable.write_text(
            dedent(
                """#!/bin/sh
                echo line 1
                echo not parsed >&2
                echo line 2
                """
            )
        )

        lines = []
        result = await exec_process(
            protocol_factory=lambda: ProcessParserProtocol(
                out_parser=lines.append
            )
        )
        assert lines == ["line 1", "line 2"]
        # Full stdout is not returned
        assert result == (None, "not parsed\n")

    @pytest.mark.asyncio
    async def test_parse_stderr(self, event_loop, executable, exec_process):
        """It's possible to pass a function to parse stderr line by line."""
        executable.write_text(
            dedent(
                """#!/bin/sh
                echo line 1 >&2
                echo not parsed
                echo line 2 >&2
                """
            )
        )

        lines = []
        result = await exec_process(
            protocol_factory=lambda: ProcessParserProtocol(
                err_parser=lines.append
            )
        )
        assert lines == ["line 1", "line 2"]
        # Full stderr is not returned
        assert result == ("not parsed\n", None)

    async def test_parse_no_ending_newline(
        self, event_loop, executable, exec_process
    ):
        """The last line of output is partse if it doesn't have a newline."""
        executable.write_text(
            dedent(
                """#!/bin/sh
                echo line 1
                echo -n line 2
                """
            )
        )

        lines = []
        await exec_process(
            protocol_factory=lambda: ProcessParserProtocol(
                out_parser=lines.append
            )
        )
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
