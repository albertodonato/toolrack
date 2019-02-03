import pytest

from ..iterate import flatten_dict


class TestFlattenDict:
    @pytest.mark.parametrize(
        "data,result",
        [
            # a dict
            ({"a": 3, "b": 4}, [("a", 3), ("b", 4)]),
            # a dict of dicts
            ({"a": {"1": 1}, "b": {"2": 2}}, [("a.1", 1), ("b.2", 2)]),
            # a dict with mixed values
            ({"a": {"1": 1}, "b": 2}, [("a.1", 1), ("b", 2)]),
            # a multi-level dict
            (
                {"a": {"1": 1, "3": {"9": "foo"}}, "b": {"2": {"x": 9}, "bar": "baz"}},
                [("a.1", 1), ("a.3.9", "foo"), ("b.2.x", 9), ("b.bar", "baz")],
            ),
        ],
    )
    def test_flatten(self, data, result):
        """Flatten handles different type of input data."""
        items = flatten_dict(data)
        assert sorted(items) == result

    def test_flatten_dict_join_char(self):
        """A custom join_char can be specified."""
        data = {"a": {"1": 1}, "b": {"2": 2}}
        items = flatten_dict(data, join_char="-")
        assert sorted(items) == [("a-1", 1), ("b-2", 2)]

    def test_flatten_dict_prefix(self):
        """A prefix can be specified."""
        data = {"a": {"1": 1}, "b": {"2": 2}}
        items = flatten_dict(data, prefix="pre")
        assert sorted(items) == [("pre.a.1", 1), ("pre.b.2", 2)]

    def test_flatten_dict_key_not_string(self):
        """If the key is not a string, it's converted to string."""
        items = flatten_dict({1: "a"})
        assert sorted(items) == [("1", "a")]
