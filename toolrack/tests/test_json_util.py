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
from json import dumps

from toolrack.testing import TestCase
from toolrack.json_util import indent


class IndentTests(TestCase):

    def setUp(self):
        super().setUp()
        self.in_fd = StringIO()
        self.out_fd = StringIO()

    def test_indent(self):
        '''JSON text is indented by 4 spaces by default.'''
        self.in_fd.write(dumps({'foo': 3, 'bar': [4, 5]}))
        self.in_fd.seek(0)
        indent(self.in_fd, self.out_fd)
        self.assertEqual(
            self.out_fd.getvalue(),
            '{\n'
            '    "bar": [\n'
            '        4,\n'
            '        5\n'
            '    ],\n'
            '    "foo": 3\n'
            '}\n')

    def test_indent_different_spaces(self):
        '''Indentation level can be changed.'''
        self.in_fd.write(dumps({'foo': 3, 'bar': [4, 5]}))
        self.in_fd.seek(0)
        indent(self.in_fd, self.out_fd, indent=2)
        self.assertEqual(
            self.out_fd.getvalue(),
            '{\n'
            '  "bar": [\n'
            '    4,\n'
            '    5\n'
            '  ],\n'
            '  "foo": 3\n'
            '}\n')

    def test_indent_ensure_ascii(self):
        '''Unicode chars can be encoded.'''
        self.in_fd.write(dumps({'foo': '\N{SNOWMAN}'}))
        self.in_fd.seek(0)
        indent(self.in_fd, self.out_fd, indent=2, ensure_ascii=True)
        self.assertEqual(
            self.out_fd.getvalue(), '{\n  "foo": "\\u2603"\n}\n')
