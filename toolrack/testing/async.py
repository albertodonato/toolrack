'''Unit-test for asynchronous code.


This module provides a :class:`LoopTestCase` class with helpers to simplify
unittesting :mod:`asincio`-based code.

'''

from functools import wraps
from asyncio import (
    get_event_loop_policy, set_event_loop_policy, set_event_loop,
    Future, ensure_future, iscoroutine)
from asyncio.events import BaseDefaultEventLoopPolicy
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
    wraps test methods declared with `async`, that behave like coroutine or
    return a :class:`Future`, so that the loop will wait for the test method to
    complete.

    This makes test code more straighforward and easier to read::

        async def test_mycoro(self):
            result = await mycoro()
            self.assertEqual(result, 'result')


    The class also provides helper methods to synchronously wait for the
    result or error of an async call::

        def test_sync(self):
            result = self.async_result(mycoro())
            error = self.async_error(myfailingcoro())

    '''

    def setUp(self):
        super().setUp()
        self._original_loop_policy = get_event_loop_policy()
        self.set_event_loop()

    def run(self, result=None):
        test_method = getattr(self, self._testMethodName)
        setattr(self, self._testMethodName, self._wrap_async(test_method))
        super().run(result=result)
        # Close the loop here since cleanups (which are called in run()) might
        # wait on async stuff too.
        self.loop.close()
        # Reset the original event loop policy
        set_event_loop_policy(self._original_loop_policy)

    def addCleanup(self, function, *args, **kwargs):
        if self._is_async(function):
            # Run the loop to wait for the function to complete, passing the
            # original function as argument.
            args = (function,) + args
            function = self.loop.run_until_complete

        super().addCleanup(function, *args, **kwargs)

    def set_event_loop(self):
        '''Set a new :class:`TestLoop` for each test.

        Can be overridden to set a different loop type.

        '''
        set_event_loop_policy(BaseDefaultEventLoopPolicy())
        self.loop = TestLoop()
        set_event_loop(self.loop)

    def async_result(self, call):
        '''Wait for the async call to complete and return its result.'''
        future = self.loop.run_until_complete(self._wrap_async_call(call))
        return future.result()

    def async_error(self, call):
        '''Wait for the async call to fail and return the exception.'''
        future = self.loop.run_until_complete(self._wrap_async_call(call))
        return future.exception()

    async def _wrap_async_call(self, call):
        '''Return a Future with the result or exception from an async call.'''
        future = Future()

        try:
            result = await call
            future.set_result(result)
        except BaseException as error:
            future.set_exception(error)

        return future

    def _wrap_async(self, method):
        '''If the method is a coroutine, wrap it and wait for it.'''

        @wraps(method)
        def wrapper():
            result = method()
            if self._is_async(result):
                self.loop.run_until_complete(
                    ensure_future(result, loop=self.loop))
            elif result is not None:
                raise RuntimeError('Test method should not return a value')

        return wrapper

    def _is_async(self, obj):
        '''Return whether an object is a coroutine or Future.'''
        return iscoroutine(obj) or isinstance(obj, Future)
