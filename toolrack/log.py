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

'''Logging helpers.

The :class:`Loggable` mixin provides a :data:`logger` attribute with a
configured logger using the class name (including the module path) as logger
name.

'''

import logging

from .property import cachedproperty

#: Default format for logging to a stream
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'


def setup_logger(name=None, stream=None, level=None, format=LOG_FORMAT):
    '''Helper to setup a logger with a default handler.

    Parameters:
        - name: the name of the logger. If not specified, the :data:`root`
          logger is used.
        - stream: an output stream for the log handler. If not specified,
          the null handler is installed.
        - level: the minimum log level for the logger.

    '''
    logger = logging.getLogger(name=name)

    if stream is None:
        handler = logging.NullHandler()
    else:
        handler = logging.StreamHandler(stream=stream)
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)

    logger.addHandler(handler)

    if level is not None:
        logger.setLevel(level)

    return logger


class Loggable:
    '''Mixin class providing a :data:`logger` attribute.'''

    @cachedproperty
    def logger(self):
        '''Return a logger for this class.'''
        logger_name = '{}.{}'.format(self.__module__, self.__class__.__name__)
        if hasattr(self, 'name'):
            logger_name += '[{}]'.format(self.name)
        return logging.getLogger(name=logger_name)
