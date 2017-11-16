"""Hold and parse key/value configurations.

The :class:`Config` describes valid configuration keys along with their types,
and performs parsing and type conversion from a dict of config options.  It
also checks required keys and applies default values if an option is not
provided.

As an example::

  config = Config(
      ConfigKey('option1', 'int', default=4),
      ConfigKey('option2', 'bool', required=True))
  config.parse({'option2': 'true'})

returns ``{'option1': 4, 'option2': True}``.

"""

from operator import attrgetter
from functools import partial


class MissingConfigKey(Exception):

    def __init__(self, key):
        super().__init__('Missing configuration key: {}'.format(key))
        self.key = key


class InvalidConfigValue(Exception):

    def __init__(self, key):
        super().__init__('Invalid value for configuration key: {}'.format(key))
        self.key = key


class ConfigKeyTypes:
    """Collection of type converters for ConfigKeys."""

    # Base types
    _type_int = int
    _type_float = float
    _type_str = str

    def get_converter(self, _type):
        """Return the converter method for the specified type."""
        if _type.endswith('[]'):
            _type = _type.strip('[]')
            elem_converter = self.get_converter(_type)
            converter = partial(self._type_list, elem_converter)
        else:
            try:
                converter = getattr(self, '_type_{}'.format(_type))
            except AttributeError:
                raise TypeError(_type)

        return converter

    def _type_bool(self, value):
        """Convert to boolean.

        Accepted values for True are 'true', 'yes' and '1', case insensitive.
        """
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1')
        return bool(value)

    def _type_list(self, converter, value):
        """Convert to list."""
        if isinstance(value, str):
            value = value.split()
        return [converter(item) for item in value]


class ConfigKey:
    """A key in the Configuration."""

    def __init__(self, name, _type, description='', required=False,
                 default=None, validator=None):
        self.name = name
        self.type = _type
        self.description = description
        self.required = required
        self.default = default
        self.validator = validator
        self.description
        self._config_types = ConfigKeyTypes()

    def parse(self, value):
        """Convert and validate a value."""
        try:
            value = self._convert(value)
            self._validate(value)
        except ValueError:
            raise InvalidConfigValue(self.name)
        return value

    def validate(self, value):
        """Validate a value based for the key.

        Can be overridden by subclasses. It should raise a ValueError if the
        value is invalid.
        """
        pass

    def _validate(self, value):
        """Call the type validator."""
        self.validate(value)
        if self.validator is not None:
            self.validator(value)

    def _convert(self, value):
        """Convert the value to the proper type."""
        converter = self._config_types.get_converter(self.type)
        return converter(value)


class Config:
    """Parse a configuration dictionary.

    A configuration has a set of keys of specific types.
    """

    def __init__(self, *keys):
        self._config_keys = {key.name: key for key in keys}

    def keys(self):
        """Return ConfigKeys sorted by name alphabetically."""
        return sorted(self._config_keys.values(), key=attrgetter('name'))

    def extend(self, *keys):
        """Return a new Config with additional keys."""
        all_keys = self._config_keys.copy()
        all_keys.update((key.name, key) for key in keys)
        return Config(*all_keys.values())

    def parse(self, config):
        """Parse the provided configuration dict.

        Returns a dict with configuration keys and values converted to the
        proper type. The dict includes only keys declared in the Config, with
        default values if not present in the config dict.
        """
        if config is None:
            config = {}

        parsed_config = {}
        for name, config_key in self._config_keys.items():
            if config_key.required and name not in config:
                raise MissingConfigKey(name)

            if name in config:
                value = config_key.parse(config[name])
            else:
                value = config_key.default
            parsed_config[name] = value

        return parsed_config
