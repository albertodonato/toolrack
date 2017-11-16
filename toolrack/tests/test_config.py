from operator import attrgetter
from unittest import TestCase

from ..config import (
    Config, ConfigKey, ConfigKeyTypes, MissingConfigKey, InvalidConfigValue)


class ConfigKeyTypesTests(TestCase):

    def setUp(self):
        super().setUp()
        self.key_types = ConfigKeyTypes()

    def test_get_converter_unknown_type(self):
        """An error is raised if type is unknown."""
        self.assertRaises(TypeError, self.key_types.get_converter, 'unknown')

    def test_int(self):
        """Value can be converted to integer."""
        converter = self.key_types.get_converter('int')
        self.assertEqual(converter('20'), 20)

    def test_float(self):
        """Value can be converted to float."""
        converter = self.key_types.get_converter('float')
        self.assertEqual(converter('20.30'), 20.30)

    def test_str(self):
        """Value can be converted to string."""
        converter = self.key_types.get_converter('str')
        self.assertEqual(converter(10), '10')

    def test_bool_true(self):
        """Values that are true return True."""
        converter = self.key_types.get_converter('bool')
        self.assertTrue(converter(3))
        self.assertTrue(converter(['foo']))

    def test_bool_false(self):
        """Values that are false return False."""
        converter = self.key_types.get_converter('bool')
        self.assertFalse(converter(0))
        self.assertFalse(converter([]))

    def test_bool_true_from_string(self):
        """Values 'true' and 'yes' accepted as True for boolean."""
        converter = self.key_types.get_converter('bool')
        self.assertTrue(converter('true'))
        self.assertTrue(converter('yes'))
        self.assertTrue(converter('True'))
        self.assertTrue(converter('Yes'))

    def test_bool_false_from_string(self):
        """Other string values are converted as False."""
        converter = self.key_types.get_converter('bool')
        self.assertFalse(converter('false'))
        self.assertFalse(converter('no'))
        self.assertFalse(converter('foo'))
        self.assertFalse(converter(''))

    def test_bool_int(self):
        """Integer values are converted to bolean."""
        converter = self.key_types.get_converter('bool')
        self.assertFalse(converter('false'))
        self.assertFalse(converter('no'))
        self.assertFalse(converter('foo'))
        self.assertFalse(converter(''))

    def test_list(self):
        """List values are converted to lists."""
        converter = self.key_types.get_converter('str[]')
        self.assertEqual(converter(('a', 'b')), ['a', 'b'])
        self.assertEqual(converter(['a', 'b']), ['a', 'b'])

    def test_list_from_string(self):
        """List values are converted to lists from strings."""
        converter = self.key_types.get_converter('str[]')
        self.assertEqual(converter('a b'), ['a', 'b'])

    def test_list_of_ints(self):
        """List values are converted to the propert list type."""
        converter = self.key_types.get_converter('int[]')
        self.assertEqual(converter('1 2'), [1, 2])

    def test_list_of_unknown(self):
        """An error is raised if a list of unknown type is requested."""
        self.assertRaises(TypeError, self.key_types.get_converter, 'unknown[]')


class ConfigKeyTests(TestCase):

    def test_instantiate(self):
        """A ConfigKey has a name."""
        config_key = ConfigKey('key', 'str')
        self.assertEqual(config_key.name, 'key')
        self.assertEqual(config_key.description, '')
        self.assertIsNone(config_key.default)
        self.assertIsNone(config_key.validator)
        self.assertFalse(config_key.required)

    def test_instantiate_with_description(self):
        """A ConfigKey can have a description."""
        config_key = ConfigKey('key', 'str', description='a config key')
        self.assertEqual(config_key.description, 'a config key')

    def test_instantiate_with_required(self):
        """A ConfigKey can be marked as required."""
        config_key = ConfigKey('key', 'str', required=True)
        self.assertTrue(config_key.required)

    def test_instantiate_with_default(self):
        """A ConfigKey can have a default value."""
        config_key = ConfigKey('key', 'str', default=9)
        self.assertEqual(config_key.default, 9)

    def test_instantiate_with_validator(self):
        """A ConfigKey can have a validator."""
        validator = object()  # just a marker
        config_key = ConfigKey('key', 'str', validator=validator)
        self.assertIs(config_key.validator, validator)

    def test_parse_string(self):
        """ConfigKey.parse parses a string value."""
        config_key = ConfigKey('key', 'str')
        self.assertEqual(config_key.parse('message'), 'message')
        self.assertEqual(config_key.parse(9), '9')

    def test_parse_int(self):
        """ConfigKey.parse parses an integer value."""
        config_key = ConfigKey('key', 'int')
        self.assertEqual(config_key.parse('100'), 100)

    def test_parse_float(self):
        """ConfigKey.parse parses a float value."""
        config_key = ConfigKey('key', 'float')
        self.assertEqual(config_key.parse('100.3'), 100.3)

    def test_parse_invalid_value(self):
        """If the type conversion fails, an error is raised."""
        config_key = ConfigKey('key', 'int')
        self.assertRaises(InvalidConfigValue, config_key.parse, 'not an int')

    def test_parse_with_validator(self):
        """If the validator fails, an error is raised."""

        def validator(value):
            raise ValueError('Wrong!')

        config_key = ConfigKey('key', 'str', validator=validator)
        self.assertRaises(InvalidConfigValue, config_key.parse, 'value')

    def test_parse_with_validate(self):
        """If the ConfigKey.validate method fails, an error is raised."""

        class ValidatedConfigKey(ConfigKey):

            def validate(self, value):
                raise ValueError('Wrong!')

        config_key = ValidatedConfigKey('key', 'str')
        self.assertRaises(InvalidConfigValue, config_key.parse, 'value')


class ConfigTests(TestCase):

    def test_keys(self):
        """Config.keys return a sorted list of ConfigKeys."""
        keys = [ConfigKey('foo', 'str'), ConfigKey('bar', 'str')]
        config = Config(*keys)
        self.assertEqual(config.keys(), sorted(keys, key=attrgetter('name')))

    def test_extend(self):
        """Config.extend returns a new Config with additional keys."""
        keys = [ConfigKey('foo', 'str'), ConfigKey('bar', 'str')]
        config = Config(*keys)
        new_keys = [ConfigKey('baz', 'str'), ConfigKey('bza', 'str')]
        new_config = config.extend(*new_keys)
        self.assertIsNot(new_config, config)
        all_keys = sorted(keys + new_keys, key=attrgetter('name'))
        self.assertEqual(new_config.keys(), all_keys)

    def test_extend_overwrite(self):
        """Config.extend overwrites configuration keys with the same name."""
        config = Config(ConfigKey('foo', 'str'))
        new_config = config.extend(ConfigKey('foo', 'int'))
        parsed = new_config.parse({'foo': '4'})
        self.assertEqual(parsed, {'foo': 4})

    def test_parse_empty(self):
        """If not config options are present, an empty dict is returned."""
        config = Config()
        self.assertEqual(config.parse({}), {})

    def test_parse_none(self):
        """If None is passed as config, an empty dict is returned."""
        config = Config()
        self.assertEqual(config.parse(None), {})

    def test_parse_converts_values(self):
        """Config.parse convert key values to their types."""
        config = Config(
            ConfigKey('foo', 'int'), ConfigKey('bar', 'float'))
        parsed = config.parse({'foo': '33', 'bar': '20.1'})
        self.assertEqual(parsed, {'foo': 33, 'bar': 20.1})

    def test_parse_unknown_key(self):
        """Config.parse ignores unknown keys."""
        config = Config(ConfigKey('foo', 'str'), ConfigKey('bar', 'str'))
        parsed = config.parse({'foo': 'Foo', 'bar': 'Bar', 'baz': '9'})
        self.assertEqual(parsed, {'foo': 'Foo', 'bar': 'Bar'})

    def test_parse_missing_key(self):
        """If a required key is missing, an error is raised."""
        config = Config(ConfigKey('foo', 'str', required=True))
        self.assertRaises(MissingConfigKey, config.parse, {})

    def test_parse_invalid_value(self):
        """Config.parse raises an error if a value is invalid."""
        config = Config(
            ConfigKey('foo', 'int'), ConfigKey('bar', 'float'))
        self.assertRaises(
            InvalidConfigValue, config.parse, {'foo': '33', 'bar': 'invalid!'})

    def test_parse_includes_defaults(self):
        """If a config key is missing, the default value is returned."""
        config = Config(
            ConfigKey('foo', 'str'), ConfigKey('bar', 'str', default=10))
        parsed = config.parse({'foo': 'Foo'})
        self.assertEqual(parsed, {'foo': 'Foo', 'bar': 10})
