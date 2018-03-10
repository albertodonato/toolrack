from .. import (
    TestCase,
    TempDirFixture,
)


class TestCaseTests(TestCase):

    def setUp(self):
        super().setUp()
        self.fixture = self.useFixture(TempDirFixture())

    def test_read_file(self):
        """readfile() returns the content of a file."""
        path = self.fixture.mkfile(content='some content')
        self.assertEqual(self.readfile(path), 'some content')
