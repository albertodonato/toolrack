import pytest

from ..convert import convert_bbyte


class TestConvertBbyte:
    def test_convert_no_conversion(self):
        """If no from/to multipliers are provided, no conversion is made."""
        assert convert_bbyte(1024) == 1024

    @pytest.mark.parametrize("suffix,value", [("kib", 1024), ("mib", 1048576)])
    def test_convert_form(self, suffix, value):
        """It's possible to convert form a multiplier to bytes."""
        assert convert_bbyte(1, suffix=suffix) == value

    @pytest.mark.parametrize("value,to", [(1073741824, "gib"), (1099511627776, "tib")])
    def test_convert_to(self, value, to):
        """It's possible to convert to a multiplier from bytes."""
        assert convert_bbyte(value, to=to) == 1

    @pytest.mark.parametrize("value,suffix", [(1024, "mib"), (1048576, "kib")])
    def test_convert_from_to(self, value, suffix):
        """It's possible to covert across multipliers."""
        assert convert_bbyte(value, suffix=suffix, to="gib") == 1

    def test_convert_unknown_suffix(self):
        """If the passed value for `suffix` is unknown, an error is raised."""
        with pytest.raises(ValueError) as error:
            convert_bbyte(100, suffix="boo")
        assert str(error.value) == "Unknown multiplier suffix"

    def test_convert_unknown_to(self):
        """If the passed value for `to` is unknown, an error is raised."""
        with pytest.raises(ValueError) as error:
            convert_bbyte(100, to="boo")
        assert str(error.value) == "Unknown target multiplier"
