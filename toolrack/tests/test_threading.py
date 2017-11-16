from threading import Thread

from ..testing import TestCase
from ..threading import ThreadLocalAttribute, thread_local_attrs


class SampleClass:

    attr = ThreadLocalAttribute('attr')

    def __init__(self, attr):
        self.attr = attr


class ThreadLocalAttributeTests(TestCase):

    def setUp(self):
        super().setUp()
        self.instance = SampleClass('value')

    def test_get_attr(self):
        """The descriptor allows getting the attribute value."""
        self.assertEqual(self.instance.attr, 'value')

    def test_set_attr(self):
        """The descriptor allows setting the attribute value."""
        self.instance.attr = 'other value'
        self.assertEqual(self.instance.attr, 'other value')

    def test_del_attr(self):
        """The descriptor allows deleting the attribute."""
        del self.instance.attr
        self.assertFalse(hasattr(self.instance, 'attr'))

    def test_thread_local(self):
        """The attribute value is thread-local."""
        thread_value = []

        def target():
            self.instance.attr = 'from thread'
            thread_value.append(self.instance.attr)

        thread = Thread(target=target)
        thread.start()
        thread.join()
        self.assertEqual(thread_value, ['from thread'])
        # In the main thread the value is unchanged
        self.assertEqual(self.instance.attr, 'value')


class ThreadLocalAttrsTests(TestCase):

    def test_decorator(self):
        """The decorator makes specified attributes thread-local."""

        @thread_local_attrs('attr1')
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
        self.assertEqual(thread_values, [10, 20])
        # The value for the decorated attribute is not changed in the main
        # thread
        self.assertEqual(instance.attr1, 1)
        # The value for the non-decorated attribute is updated
        self.assertEqual(instance.attr2, 20)
