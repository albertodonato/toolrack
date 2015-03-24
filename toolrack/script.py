#
# This file is part of ToolRack.

# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Base class for python scripts.

This module provides a :class:`Script` class to reduce boilerplate when
creating python scripts.

:class:`Script` instances are callable, and can optionally receive a list of
arguments (by default they look at :data:`sys.argv`).

A typical use of :class:`Script` is to declare a subclass with the script
logic and create an instance::

  class MyScript(Script):

      def main(self, args):
         # script logic here
         ...

  my_script = MyScript()

The instance can be referenced in :mod:`setuptools` ``entry_points`` key::

  setup(
      entry_points={'console_scripts': ['my_script=path.to.script:my_script']},
      ...)

'''

import sys


class ErrorExitMessage(Exception):
    '''Raised to exit the process with the specified message and exit code.

    Parameters:
        - message: the error message.
        - code: the script exit code.

    '''

    def __init__(self, message, code=1):
        super(ErrorExitMessage, self).__init__(message)
        self.code = code


class Script(object):
    '''Wraps a python script handling argument parsing.

    Subclasses must implement :func:`get_parser` and :func:`main` methods.

    Inside :func:`main`, :exc:`ErrorExitMessage` can be raised with the
    appropriate ``message`` and ``code`` to cause the script termination, with
    the message outputted to standard error.

    Script instances are callable, and can be passed the argument list (which
    defaults to :data:`sys.argv` if not provided).

    '''

    _exit = sys.exit

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def get_parser(self):
        '''Return a configured :class:`argparse.ArgumentParser` instance.

        .. note::
            Subclasses must implement this method.

        '''
        raise NotImplementedError()

    def main(self, args):
        '''The body of the script.

        It gets called with the :class:`argparse.Namespace` instance returned
        by :func:`get_parser`.

        Parameters:
            - args: a :class:`argparse.Namespace` with the command line.

        .. note::
            Subclasses must implement this method.

        '''
        raise NotImplementedError()

    def __call__(self, args=None):
        '''Call the script, passing sys.argv by default.'''
        parser = self.get_parser()
        parsed_args = parser.parse_args(args=args)
        try:
            self.main(parsed_args)
        except ErrorExitMessage as error:
            self._error_exit(error)

    def _error_exit(self, error):
        '''Terminate with the specified ErrorExitMessage.'''
        self._stderr.write('{}\n'.format(error.message))
        self._exit(error.code)
