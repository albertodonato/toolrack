from io import StringIO
from json import dumps
from textwrap import dedent

from ..json_util import indent


class TestIndent:
    def test_indent(self):
        """JSON text is indented by 4 spaces by default."""
        in_fd, out_fd = StringIO(), StringIO()
        in_fd.write(dumps({"foo": 3, "bar": [4, 5]}))
        in_fd.seek(0)
        indent(in_fd, out_fd)
        assert out_fd.getvalue() == dedent(
            """\
            {
                "bar": [
                    4,
                    5
                ],
                "foo": 3
            }
            """
        )

    def test_indent_different_spaces(self):
        """Indentation level can be changed."""
        in_fd, out_fd = StringIO(), StringIO()
        in_fd.write(dumps({"foo": 3, "bar": [4, 5]}))
        in_fd.seek(0)
        indent(in_fd, out_fd, indent=2)
        assert out_fd.getvalue() == dedent(
            """\
            {
              "bar": [
                4,
                5
              ],
              "foo": 3
            }
            """
        )

    def test_indent_ensure_ascii(self):
        """Unicode chars can be encoded."""
        in_fd, out_fd = StringIO(), StringIO()
        in_fd.write(dumps({"foo": "\N{SNOWMAN}"}))
        in_fd.seek(0)
        indent(in_fd, out_fd, indent=2, ensure_ascii=True)
        assert out_fd.getvalue() == dedent(
            """\
            {
              "foo": "\\u2603"
            }
            """
        )
