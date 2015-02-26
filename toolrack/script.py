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

'''A base class for python scripts.


Subclasses of Script must implement the following methods:

 - get_parser(): it must return an argparser.ArgumentParser instance,
   configured with the proper options/arguments that the script handles.  - -

 - main(args): the actual script code, it gets called with the
   argparse.Namespace instance returned by the parser.

Inside main, Scripts can raise ErrorExitMessage with the appropriate message
and code to cause the program termination.

Script instances are callable, and can be passed the argument list (which
defaults to sys.argv if not provided).

'''

import sys


class ErrorExitMessage(Exception):
    '''Raised to exit the process with the specified message and exit code.'''

    def __init__(self, message, code=1):
        super(ErrorExitMessage, self).__init__(message)
        self.code = code


class Script(object):
    '''Wraps a python script handling argument parsing.'''

    exit = sys.exit

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self._stdout = stdout
        self._stderr = stderr

    def get_parser(self):
        '''Return a configured argparse.ArgumentParser instance.'''
        raise NotImplementedError()

    def main(self, args):
        '''Body of the script.

        It gets called with the argparse.Namespace instance returned by
        get_parser.

        '''
        raise NotImplementedError()

    def __call__(self, args=None):
        parser = self.get_parser()
        parsed_args = parser.parse_args(args=args)
        try:
            self.main(parsed_args)
        except ErrorExitMessage as error:
            self._error_exit(error)

    def _error_exit(self, error):
        '''Terminate with the specified ErrorExitMessage.'''
        self._stderr.write(error.message + '\n')
        self.exit(error.code)
