from threading import Thread

import pytest

from ..threading import (
    thread_local_attrs,
    ThreadLocalAttribute,
)


class SampleClass:

    attr = ThreadLocalAttribute("attr")

    def __init__(self, attr):
        self.attr = attr


@pytest.fixture
def instance():
    yield SampleClass("value")


class TestThreadLocalAttribute:
    def test_get_attr(self, instance):
        """The descriptor allows getting the attribute value."""
        assert instance.attr == "value"

    def test_set_attr(self, instance):
        """The descriptor allows setting the attribute value."""
        instance.attr = "other value"
        assert instance.attr == "other value"

    def test_del_attr(self, instance):
        """The descriptor allows deleting the attribute."""
        del instance.attr
        assert not hasattr(instance, "attr")

    def test_thread_local(self, instance):
        """The attribute value is thread-local."""
        thread_value = []

        def target():
            instance.attr = "from thread"
            thread_value.append(instance.attr)

        thread = Thread(target=target)
        thread.start()
        thread.join()
        assert thread_value == ["from thread"]
        # In the main thread the value is unchanged
        assert instance.attr == "value"


class TestThreadLocalAttrs:
    def test_decorator(self):
        """The decorator makes specified attributes thread-local."""

        @thread_local_attrs("attr1")
        class DecoratedSampleClass:
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

        instance = DecoratedSampleClass(1, 2)
        thread_values = []

        def target():
            instance.attr1 = 10
            instance.attr2 = 20
            thread_values.extend((instance.attr1, instance.attr2))

        thread = Thread(target=target)
        thread.start()
        thread.join()
        assert thread_values == [10, 20]
        # The value for the decorated attribute is not changed in the main
        # thread
        assert instance.attr1 == 1
        # The value for the non-decorated attribute is updated
        assert instance.attr2 == 20
