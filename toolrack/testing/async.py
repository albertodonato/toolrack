#
# This file is part of ToolRack.
#
# ToolRack is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ToolRack is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ToolRack.  If not, see <http://www.gnu.org/licenses/>.

'''Unit-test for asynchronous code.


This module provides a :class:`LoopTestCase` class with helpers to simplify
unittesting :mod:`asincio`-based code.

'''

from functools import wraps
from asyncio import set_event_loop, Future, coroutine, iscoroutine, async
from asyncio.test_utils import TestLoop as AsyncioTestLoop

from . import TestCase


class TestLoop(AsyncioTestLoop):
    '''Test loop which schedules a run when time is advanced.

    Tests can call the :meth:`advance()` method to move the time forward.
    For instance::

        loop = TestLoop()
        loop.call_at(5, callback)
        loop.advance(5)  # callback gets executed

    '''

    def __init__(self):
        super().__init__(gen=self._gen)

    def advance(self, advance):
        '''Advance the loop time and schedule a run.'''
        assert advance >= 0, 'Time advance must not be negative'
        self.advance_time(advance)
        self._run_once()

    def create_task(self, coro):
        '''Create a task from a coroutine.

        The loop is run to consume all pending ready callbacks that can be
        created by the added task.

        '''
        task = super().create_task(coro)
        # Execute the task
        while self._ready:
            self._run_once()
        return task

    def _gen(self):
        '''Generator for the TestLoop.'''
        absolute_time = -1
        while absolute_time:
            absolute_time = yield 0


class LoopTestCase(TestCase):
    '''Base test class for tests requiring an :mod:`asyncio` loop.

    It uses a :class:`TestLoop`, so that it's possible to manually advance time
    in tests.

    Beside providing a separate `loop` for each test, the class automatically
    wraps test methods that behave like coroutine or return a :class:`Future`,
    so that the loop will wait for the test method to complete.

    This makes test code more straighforward and easier to read::

        def test_mycoro(self):
            result = yield form mycoro()
            self.assertEqual(result, 'result')


    The class also provides helper methods to synchronously wait for the
    result or error of an async call::

        def test_sync(self):
            result = self.async_result(mycoro())
            error = self.async_error(myfailingcoro())

    '''

    def setUp(self):
        super().setUp()
        # Use new event loop for each test
        self.loop = TestLoop()
        set_event_loop(self.loop)
        self.addCleanup(self.loop.close)

    def run(self, result=None):
        test_method = getattr(self, self._testMethodName)
        setattr(self, self._testMethodName, self._wrap_async(test_method))
        return super().run(result=result)

    def async_result(self, call):
        '''Wait for the async call to complete and return its result.'''
        future = self.loop.run_until_complete(self._wrap_async_call(call))
        return future.result()

    def async_error(self, call):
        '''Wait for the async call to fail and return the exception.'''
        future = self.loop.run_until_complete(self._wrap_async_call(call))
        return future.exception()

    @coroutine
    def _wrap_async_call(self, call):
        '''Return a Future with the result or exception from an async call.'''
        future = Future()

        try:
            result = yield from call
            future.set_result(result)
        except BaseException as error:
            future.set_exception(error)

        return future

    def _wrap_async(self, method):
        '''If the method is a coroutine, wrap it and wait for it.'''

        @wraps(method)
        def wrapper():
            result = method()
            if iscoroutine(result) or isinstance(result, Future):
                self.loop.run_until_complete(async(result, loop=self.loop))
            elif result is not None:
                raise RuntimeError('Test method should not return a value')

        return wrapper