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
import json

from toolrack.script import Script, ErrorExitMessage


class JSONIndent(Script):

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
            self._indent(args.input, args.output, args.num, args.ascii)
        except ValueError as error:
            raise ErrorExitMessage('Indenting failed: {}'.format(error))
        except KeyboardInterrupt:
            pass

    def _indent(self, in_stream, out_stream, indent, ensure_ascii):
        data = json.load(in_stream)
        json.dump(
            data, out_stream, sort_keys=True, ensure_ascii=ensure_ascii,
            indent=indent)
        out_stream.write('\n')


script = JSONIndent()
