from ..async import LoopTestCase


class AsyncTests(LoopTestCase):

    def test_advance(self):
        '''TestLoop.advance advances time and runs the loop.'''
        calls = []

        def callback():
            calls.append(self.loop.time())

        self.loop.call_later(5, callback)
        self.loop.call_later(10, callback)
        self.loop.advance(5)
        self.assertEqual(calls, [5])
        self.loop.advance(5)
        self.assertEqual(calls, [5, 10])

    def test_create_task(self):
        '''TestLoop.create_task immediately executes the task.'''

        async def coro():
            return 'result'

        task = self.loop.create_task(coro())
        self.assertEqual(task.result(), 'result')

    def test_async_result(self):
        '''TestLoop.async_result returns the result of the coroutine.'''

        async def coro():
            return 'result'

        result = self.async_result(coro())
        self.assertEqual(result, 'result')

    def test_async_error(self):
        '''TestLoop.async_error returns the error raised by the coroutine.'''

        async def coro():
            raise Exception('failed')

        error = self.async_error(coro())
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), 'failed')
