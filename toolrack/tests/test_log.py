from io import StringIO
import logging

from ..log import (
    Loggable,
    setup_logger,
)


class SampleLoggable(Loggable):

    name = "loggable"


class TestSetupLogger:
    def test_setup_with_name(self, caplog):
        """If a name is specified for the logger, it is set up."""
        with caplog.at_level(logging.INFO):
            logger = setup_logger(name="test-logger")
            assert logger.name == "test-logger"
            logger.info("log message")
        assert caplog.record_tuples == [("test-logger", logging.INFO, "log message")]

    def test_setup_level(self, caplog):
        """If specified, a level is set on the logger."""
        with caplog.at_level(logging.DEBUG):
            logger = setup_logger(level=logging.ERROR)
            logger.info("info message")
        # The info message is not recorded
        assert caplog.records == []

    def test_setup_stream(self, caplog):
        """If a stream is specified, logging is sent to it."""
        stream = StringIO()
        with caplog.at_level(logging.INFO):
            logger = setup_logger(name="test-logger", stream=stream)
            logger.info("message")
        log = stream.getvalue()
        assert log.endswith("INFO - test-logger - message\n")


class TestLoggable:
    def test_logger_with_name(self, caplog):
        """The logger for Loggable logs the name of the class."""
        stream = StringIO()
        with caplog.at_level(logging.INFO):
            setup_logger(stream=stream)
            loggable = SampleLoggable()
            loggable.logger.info("info message")
        assert "toolrack.tests.test_log.SampleLoggable[loggable]" in stream.getvalue()
