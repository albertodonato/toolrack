from ..property import cachedproperty


class SampleClass:
    def __init__(self, value=True):
        self.value = value
        self.calls = 0

    @cachedproperty
    def property(self):
        self.calls += 1
        return self.value


class TestCachedproperty:
    def test_single_call(self):
        """The property function is called just once."""
        obj = SampleClass()
        obj.property
        obj.property
        assert obj.calls == 1

    def test_value(self):
        """The property returns the value from the method."""
        obj = SampleClass(value=100)
        assert obj.property == 100
