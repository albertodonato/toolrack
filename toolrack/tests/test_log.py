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

from io import StringIO
import logging

from fixtures import LoggerFixture

from ..testing import TestCase
from ..log import setup_logger, Loggable


class SampleLoggable(Loggable):

    name = 'loggable'


class SetupLoggerTests(TestCase):

    def setUp(self):
        super().setUp()
        self.logger = self.useFixture(LoggerFixture(level=logging.DEBUG))

    def test_setup_with_name(self):
        '''If a name is specified for the logger, it is set up.'''
        logger = setup_logger(name='test-logger')
        self.assertEqual(logger.name, 'test-logger')
        logger.info('log message')
        self.assertEqual(self.logger.output, 'log message\n')

    def test_setup_level(self):
        '''If specified, a level is set on the logger.'''
        logger = setup_logger(level=logging.ERROR)
        logger.info('info message')
        # The info message is not recorded
        self.assertEqual(self.logger.output, '')

    def test_setup_stream(self):
        '''If a stream is specified, logging is sent to it.'''
        stream = StringIO()
        logger = setup_logger(name='test-logger', stream=stream)
        logger.info('message')
        log = stream.getvalue()
        self.assertTrue(log.endswith('INFO - test-logger - message\n'))


class LoggableTests(TestCase):

    def setUp(self):
        super().setUp()
        self.logger = self.useFixture(LoggerFixture(level=logging.DEBUG))

    def test_logger_with_name(self):
        '''The logger for Loggable logs the name of the class.'''
        stream = StringIO()
        setup_logger(stream=stream)
        loggable = SampleLoggable()
        loggable.logger.info('info message')
        self.assertIn(
            'toolrack.tests.test_log.SampleLoggable[loggable]',
            stream.getvalue())
