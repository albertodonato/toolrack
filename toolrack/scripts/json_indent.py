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

'''Indent JSON text.'''

import sys
import argparse

from toolrack.json_util import indent
from toolrack.script import Script, ErrorExitMessage


class JSONIndent(Script):
    '''Script to indent JSON text.'''

    def get_parser(self):
        parser = argparse.ArgumentParser(description='Indent JSON text')
        parser.add_argument(
            '-n', '--num', metavar='N', type=int, default=2,
            help='number of indentation spaces (default: %(default)s)')
        parser.add_argument(
            '-a', '--ascii', action='store_true', default=False,
            help='force ascii output (default: %(default)s)')
        parser.add_argument(
            'input', nargs='?', type=argparse.FileType(), default=sys.stdin,
            help='input file')
        parser.add_argument(
            'output', nargs='?', type=argparse.FileType('w'),
            default=sys.stdout, help='output file')
        return parser

    def main(self, args):
        try:
            indent(
                args.input, args.output, indent=args.num,
                ensure_ascii=args.ascii)
        except ValueError as error:
            raise ErrorExitMessage('Formatting failed: {}'.format(error))
        except KeyboardInterrupt:
            pass


script = JSONIndent()
