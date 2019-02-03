from operator import attrgetter

import pytest

from ..config import (
    Config,
    ConfigKey,
    ConfigKeyTypes,
    InvalidConfigValue,
    MissingConfigKey,
)


class TestConfigKeyTypes:
    def test_get_converter_unknown_type(self):
        """An error is raised if type is unknown."""
        with pytest.raises(TypeError):
            ConfigKeyTypes().get_converter("unknown")

    @pytest.mark.parametrize(
        "conv_type,value,result",
        [("int", "10", 10), ("float", "20.30", 20.30), ("str", 10, "10")],
    )
    def test_types(self, conv_type, value, result):
        """Values can be converted."""
        converter = ConfigKeyTypes().get_converter(conv_type)
        assert converter(value) == result

    @pytest.mark.parametrize(
        "value,result",
        [
            # true values
            (3, True),
            (["foo"], True),
            ("true", True),
            ("True", True),
            ("yes", True),
            ("Yes", True),
            # false values
            (0, False),
            ([], False),
            ("false", False),
            ("no", False),
            ("foo", False),
            ("", False),
        ],
    )
    def test_bool(self, value, result):
        """Bool values cna be converted."""
        converter = ConfigKeyTypes().get_converter("bool")
        assert converter(value) == result

    @pytest.mark.parametrize("value", [("a", "b"), ["a", "b"], "a b"])
    def test_list(self, value):
        """List values are converted to lists."""
        converter = ConfigKeyTypes().get_converter("str[]")
        assert converter(value) == ["a", "b"]

    def test_list_of_ints(self):
        """List values are converted to the propert list type."""
        converter = ConfigKeyTypes().get_converter("int[]")
        assert converter("1 2") == [1, 2]

    def test_list_of_unknown(self):
        """An error is raised if a list of unknown type is requested."""
        with pytest.raises(TypeError):
            ConfigKeyTypes().get_converter("unknown[]")


class TestConfigKey:
    def test_instantiate(self):
        """A ConfigKey has a name."""
        config_key = ConfigKey("key", "str")
        assert config_key.name == "key"
        assert config_key.description == ""
        assert config_key.default is None
        assert config_key.validator is None
        assert not config_key.required

    def test_instantiate_with_description(self):
        """A ConfigKey can have a description."""
        config_key = ConfigKey("key", "str", description="a config key")
        assert config_key.description == "a config key"

    def test_instantiate_with_required(self):
        """A ConfigKey can be marked as required."""
        config_key = ConfigKey("key", "str", required=True)
        assert config_key.required

    def test_instantiate_with_default(self):
        """A ConfigKey can have a default value."""
        config_key = ConfigKey("key", "str", default=9)
        assert config_key.default == 9

    def test_instantiate_with_validator(self):
        """A ConfigKey can have a validator."""
        validator = object()  # just a marker
        config_key = ConfigKey("key", "str", validator=validator)
        assert config_key.validator is validator

    @pytest.mark.parametrize(
        "conv_type,value,result",
        [
            ("str", "message", "message"),
            ("str", 9, "9"),
            ("int", "100", 100),
            ("float", "100.3", 100.3),
        ],
    )
    def test_parse(self, conv_type, value, result):
        """ConfigKey.parse parses values based on type."""
        config_key = ConfigKey("key", conv_type)
        assert config_key.parse(value) == result

    def test_parse_invalid_value(self):
        """If the type conversion fails, an error is raised."""
        config_key = ConfigKey("key", "int")
        with pytest.raises(InvalidConfigValue):
            config_key.parse("not an int")

    def test_parse_with_validator(self):
        """If the validator fails, an error is raised."""

        def validator(value):
            raise ValueError("Wrong!")

        config_key = ConfigKey("key", "str", validator=validator)
        with pytest.raises(InvalidConfigValue):
            config_key.parse("value")

    def test_parse_with_validate(self):
        """If the ConfigKey.validate method fails, an error is raised."""

        class ValidatedConfigKey(ConfigKey):
            def validate(self, value):
                raise ValueError("Wrong!")

        config_key = ValidatedConfigKey("key", "str")
        with pytest.raises(InvalidConfigValue):
            config_key.parse("value")


class TestConfig:
    def test_keys(self):
        """Config.keys return a sorted list of ConfigKeys."""
        keys = [ConfigKey("foo", "str"), ConfigKey("bar", "str")]
        config = Config(*keys)
        assert config.keys() == sorted(keys, key=attrgetter("name"))

    def test_extend(self):
        """Config.extend returns a new Config with additional keys."""
        keys = [ConfigKey("foo", "str"), ConfigKey("bar", "str")]
        config = Config(*keys)
        new_keys = [ConfigKey("baz", "str"), ConfigKey("bza", "str")]
        new_config = config.extend(*new_keys)
        assert new_config is not config
        all_keys = sorted(keys + new_keys, key=attrgetter("name"))
        assert new_config.keys() == all_keys

    def test_extend_overwrite(self):
        """Config.extend overwrites configuration keys with the same name."""
        config = Config(ConfigKey("foo", "str"))
        new_config = config.extend(ConfigKey("foo", "int"))
        parsed = new_config.parse({"foo": "4"})
        assert parsed == {"foo": 4}

    def test_parse_empty(self):
        """If not config options are present, an empty dict is returned."""
        config = Config()
        assert config.parse({}) == {}

    def test_parse_none(self):
        """If None is passed as config, an empty dict is returned."""
        config = Config()
        assert config.parse(None) == {}

    def test_parse_converts_values(self):
        """Config.parse convert key values to their types."""
        config = Config(ConfigKey("foo", "int"), ConfigKey("bar", "float"))
        parsed = config.parse({"foo": "33", "bar": "20.1"})
        assert parsed == {"foo": 33, "bar": 20.1}

    def test_parse_unknown_key(self):
        """Config.parse ignores unknown keys."""
        config = Config(ConfigKey("foo", "str"), ConfigKey("bar", "str"))
        parsed = config.parse({"foo": "Foo", "bar": "Bar", "baz": "9"})
        assert parsed == {"foo": "Foo", "bar": "Bar"}

    def test_parse_missing_key(self):
        """If a required key is missing, an error is raised."""
        config = Config(ConfigKey("foo", "str", required=True))
        with pytest.raises(MissingConfigKey):
            config.parse({})

    def test_parse_invalid_value(self):
        """Config.parse raises an error if a value is invalid."""
        config = Config(ConfigKey("foo", "int"), ConfigKey("bar", "float"))
        with pytest.raises(InvalidConfigValue):
            config.parse({"foo": "33", "bar": "invalid!"})

    def test_parse_includes_defaults(self):
        """If a config key is missing, the default value is returned."""
        config = Config(ConfigKey("foo", "str"), ConfigKey("bar", "str", default=10))
        parsed = config.parse({"foo": "Foo"})
        assert parsed == {"foo": "Foo", "bar": 10}
