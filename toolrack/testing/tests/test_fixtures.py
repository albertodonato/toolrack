from .. import (
    TestCase,
    TempDirFixture,
)


class TempDirFixtureTests(TestCase):

    def setUp(self):
        super().setUp()
        self.fixture = self.useFixture(TempDirFixture())

    def test_join(self):
        """join() joins paths under the fixture dir."""
        full_path = self.fixture.join('foo', 'bar', 'baz')
        self.assertEqual(
            full_path, self.fixture.path / 'foo' / 'bar' / 'baz')

    def test_mkdir(self):
        """mkdir() creates a directory."""
        path = self.fixture.mkdir('foo')
        self.assertTrue(path.is_dir())
        self.assertEqual(path, self.fixture.path / 'foo')

    def test_mkdir_path_tuple(self):
        """mkdir() creates a directory with the path specified as a tuple."""
        path = self.fixture.mkdir(('foo', 'bar'))
        self.assertTrue(path.is_dir())
        self.assertEqual(path, self.fixture.path / 'foo' / 'bar')

    def test_mkdir_no_absolute_path(self):
        """mkdir() raises an error if the path is absolute."""
        with self.assertRaises(ValueError) as cm:
            self.fixture.mkdir('/foo')
        self.assertEqual(str(cm.exception), 'Path must be relative')

    def test_mkfile(self):
        """mkfile() creates a file."""
        path = self.fixture.mkfile('foo')
        self.assertTrue(path.is_file())

    def test_mkfile_path_tuple(self):
        """mkfile() creates a file with the path specified as a tuple."""
        path = self.fixture.mkfile(('foo', 'bar'))
        self.assertTrue(path.is_file())
        self.assertEqual(path, self.fixture.path / 'foo' / 'bar')

    def test_mkfile_no_absolute_path(self):
        """mkfile() raises an error if the path is absolute."""
        with self.assertRaises(ValueError) as cm:
            self.fixture.mkfile('/foo')
        self.assertEqual(str(cm.exception), 'Path must be relative')

    def test_mkfile_content(self):
        """mkfile() creates a file with specified content."""
        path = self.fixture.mkfile('foo', content='some content')
        self.assertEqual(path.read_text(), 'some content')

    def test_mkfile_mode(self):
        """mkfile() creates a file with specified mode."""
        path = self.fixture.mkfile('foo', mode=0o700)
        mode = path.stat().st_mode & 0o777
        self.assertEqual(mode, 0o700)

    def test_mksymlink(self):
        """mksymlink() creates a symlink to the target."""
        target = self.fixture.mkfile()
        link = self.fixture.mksymlink(target)
        self.assertEqual(link.parent, self.fixture.path)
        self.assertTrue(link.is_symlink())

    def test_mksymlink_name(self):
        """mksymlink() creates a symlink with specified name."""
        target = self.fixture.mkfile()
        link = self.fixture.mksymlink(target, path='foo')
        self.assertEqual(link, self.fixture.path / 'foo')
        self.assertTrue(link.is_symlink())
