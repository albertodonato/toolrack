"""Indent JSON text."""

import sys
from argparse import ArgumentParser, FileType

from ..json_util import indent
from ..script import Script, ErrorExitMessage


class JSONIndent(Script):
    """Script to indent JSON text."""

    def get_parser(self):
        parser = ArgumentParser(description='Indent JSON text')
        parser.add_argument(
            '-n', '--num', metavar='N', type=int, default=2,
            help='number of indentation spaces (default: %(default)s)')
        parser.add_argument(
            '-a', '--ascii', action='store_true', default=False,
            help='force ascii output (default: %(default)s)')
        parser.add_argument(
            'input', nargs='?', type=FileType(), default=sys.stdin,
            help='input file')
        parser.add_argument(
            'output', nargs='?', type=FileType('w'), default=sys.stdout,
            help='output file')
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
