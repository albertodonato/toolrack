from ...testing.async import LoopTestCase
from ..periodic import PeriodicCall


class PeriodicCallTests(LoopTestCase):

    def setUp(self):
        super().setUp()
        self.calls = []
        self.periodic_call = PeriodicCall(self.loop, self.calls.append, True)

    def test_running(self):
        '''The PeriodicCall is not running by default.'''
        self.assertFalse(self.periodic_call.running)
        self.periodic_call.start(5)
        self.addCleanup(self.periodic_call.stop())
        self.assertTrue(self.periodic_call.running)

    def test_start(self):
        '''Starting the PeriodicCall makes it call the function immediately.'''
        self.periodic_call.start(5)
        self.assertEqual(self.calls, [True])

    async def test_stop(self):
        '''Stopping the PeriodicCall stops periodic runs.'''
        self.periodic_call.start(5)
        await self.periodic_call.stop()
        self.loop.advance(5)
        # Only the initial call is performed
        self.assertEqual(self.calls, [True])

    def test_periodic(self):
        '''The PeriodicCall gets called at each interval.'''
        self.periodic_call.start(5)
        self.loop.advance(5)
        self.assertEqual(self.calls, [True, True])
        self.loop.advance(5)
        self.assertEqual(self.calls, [True, True, True])

    def test_start_later(self):
        '''If now is False, the function is not run immediately.'''
        self.periodic_call.start(5, now=False)
        self.assertEqual(self.calls, [])

    def test_start_later_run_after_interval(self):
        '''If now is False, the function is run after the interval.'''
        self.periodic_call.start(5, now=False)
        self.loop.advance(5)
        self.assertEqual(self.calls, [True])

    async def test_func_arguments(self):
        '''Specified arguments are passed to the function on call.'''

        def func(*args, **kwargs):
            self.calls.append((args, kwargs))

        periodic_call = PeriodicCall(
            self.loop, func, 'foo', 'bar', baz='baz', bza='bza')
        periodic_call.start(5)
        await periodic_call.stop()
        [call] = self.calls
        self.assertEqual((('foo', 'bar'), {'baz': 'baz', 'bza': 'bza'}), call)
