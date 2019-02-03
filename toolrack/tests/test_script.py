from argparse import ArgumentParser
from io import StringIO

import pytest

from ..script import (
    ErrorExitMessage,
    Script,
)


class DummyScript(Script):

    called = False
    code = None
    args = None
    failure = None

    def get_parser(self):
        parser = ArgumentParser()
        parser.add_argument("--foo", type=int)
        return parser

    def main(self, args):
        self.called = True
        self.args = args
        if self.failure is not None:
            raise self.failure

    def _exit(self, code):
        self.code = code


class TestErrorExitMessage:
    def test_message(self):
        """ErrorExitMessage provides a message and a default code."""
        message = "Something went wrong!"
        error = ErrorExitMessage(message)
        assert error.message == message
        assert str(error) == message
        assert error.code == 1

    def test_code(self):
        """ErrorExitMessage can provide a different error code."""
        error = ErrorExitMessage("Something went wrong!", code=3)
        assert error.code == 3


@pytest.fixture
def stderr():
    yield StringIO()


@pytest.fixture
def script(stderr):
    yield DummyScript(stderr=stderr)


class TestScript:
    def test_get_parser_not_implemented(self):
        """get_parser() raises a NotImplementedError by default."""
        with pytest.raises(NotImplementedError):
            Script().get_parser()

    def test_main_not_implemented(self):
        """main() raises a NotImplementedError by default."""
        with pytest.raises(NotImplementedError):
            Script().main(None)

    def test_call_runs_main(self, script):
        """When a Script is called, the main method is executed."""
        script([])
        assert script.called
        assert script.code is None

    def test_call_parse_args(self, script, stderr):
        """When a Script is called, get_parser parses the arguments."""
        script(["--foo", "3"])
        assert script.args.foo == 3
        assert stderr.getvalue() == ""

    def test_failure(self, script, stderr):
        """If ErrorExitMessage is raised, the script is terminated."""
        script.failure = ErrorExitMessage("Fail!", code=3)
        script([])
        assert stderr.getvalue() == "Fail!\n"
        assert script.code == 3

    def test_exit(self, script):
        """Script.exit exits the process with 0 as return code."""
        calls = []
        script._exit = calls.append
        script.exit()
        assert calls == [0]

    def test_exit_with_code(self, script):
        """Script.exit exits the process with the specified return code."""
        calls = []
        script._exit = calls.append
        script.exit(code=4)
        assert calls == [4]

    def test_handle_keyboard_interrupt(self, script):
        """Script.handle_keyboard_interrupt exits cleanly by default."""
        calls = []
        script._exit = calls.append
        script.handle_keyboard_interrupt(KeyboardInterrupt())
        assert calls == [0]

    def test_handle_keyboard_interrupt_called(self, script):
        """Script.handle_keyboard_interrupt is called on KeyboardInterrupt."""
        interrupt = KeyboardInterrupt()
        calls = []
        script.failure = interrupt
        script.handle_keyboard_interrupt = calls.append
        script([])
        assert calls == [interrupt]
