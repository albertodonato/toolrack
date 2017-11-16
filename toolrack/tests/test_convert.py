from unittest import TestCase

from ..convert import convert_bbyte


class ConvertBbyteTests(TestCase):

    def test_convert_no_conversion(self):
        """If no from/to multipliers are provided, no conversion is made."""
        self.assertEqual(convert_bbyte(1024), 1024)

    def test_convert_form(self):
        """It's possible to convert form a multiplier to bytes."""
        self.assertEqual(convert_bbyte(1, suffix='kib'), 1024)
        self.assertEqual(convert_bbyte(1, suffix='mib'), 1048576)

    def test_convert_to(self):
        """It's possible to convert to a multiplier from bytes."""
        self.assertEqual(convert_bbyte(1073741824, to='gib'), 1)
        self.assertEqual(convert_bbyte(1099511627776, to='tib'), 1)

    def test_convert_from_to(self):
        """It's possible to covert across multipliers."""
        self.assertEqual(convert_bbyte(1024, suffix='mib', to='gib'), 1)
        self.assertEqual(convert_bbyte(1048576, suffix='kib', to='gib'), 1)

    def test_convert_unknown_suffix(self):
        """If the passed value for `suffix` is unknown, an error is raised."""
        with self.assertRaises(ValueError) as error:
            convert_bbyte(100, suffix='boo')
        self.assertEqual(str(error.exception), 'Unknown multiplier suffix')

    def test_convert_unknown_to(self):
        """If the passed value for `to` is unknown, an error is raised."""
        with self.assertRaises(ValueError) as error:
            convert_bbyte(100, to='boo')
        self.assertEqual(str(error.exception), 'Unknown target multiplier')
