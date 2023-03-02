"""Utilities based on the asyncio library.

This modules provides :class:`TimedCall` and :class:`PeriodicCall` classes for
timed and periodical tasks execution.

"""

from asyncio import (
    get_event_loop,
    Handle,
    iscoroutinefunction,
    Task,
)
from collections.abc import (
    Callable,
    Iterator,
)
from functools import partial
from typing import (
    cast,
    Union,
)


class AlreadyRunning(Exception):
    """The TimedCall is already running."""

    def __init__(self):
        super().__init__("Timed call is already running")


class NotRunning(Exception):
    """The TimedCall is not running."""

    def __init__(self):
        super().__init__("Timed call is not running")


TimesIterator = Iterator[Union[float, int]]


class TimedCall:
    """Call a function based on a timer.

    The class takes a function with optional arguments. Upon
    :meth:`start()`, the function is scheduled at specified times
    until :meth:`stop()` is called (or the time iterator is exausted).

    :param func: the function to call periodically.
    :param args: arguments to pass to the function.
    :param kwargs: keyword arguments to pass to the function.

    """

    def __init__(self, func: Callable, *args, **kwargs):
        self._func = self._wrap_func(func, *args, **kwargs)
        self._loop = get_event_loop()
        self._handle: Handle | None = None
        self._task: Task | None = None

    @property
    def running(self) -> bool:
        """Whether the PeriodicCall is currently running."""
        return self._handle is not None

    def start(self, times_iter: TimesIterator):
        """Start calling the function at specified times.

        :param times_iter: an iterable yielding times to execute the function
          at. If the iterator exhausts, the TimedCall is stopped.  Times must be
          compatible with :meth:`loop.time()`.

        """
        if self.running:
            raise AlreadyRunning()

        self._run(times_iter, do_call=False)

    async def stop(self):
        """Stop calling the function periodically."""
        if not self.running:
            raise NotRunning()

        if self._handle:
            self._handle.cancel()
            self._handle = None
        if self._task:
            await self._task
            self._task = None

    def _run(self, times_iter: TimesIterator, do_call: bool = True):
        if do_call:
            self._task = self._loop.create_task(self._func())
        self._schedule_next_run(times_iter)

    def _schedule_next_run(self, times_iter: TimesIterator):
        delay = self._get_run_delay(times_iter)
        if delay is None:
            self._handle = None
        else:
            self._handle = self._loop.call_later(delay, self._run, times_iter)

    def _get_run_delay(self, times_iter: TimesIterator) -> float | None:
        now = self._loop.time()
        next_time: float | int = -1
        while next_time < now:
            try:
                next_time = next(times_iter)
            except StopIteration:
                return None
        return float(next_time - now)

    def _wrap_func(self, func: Callable, *args, **kwargs) -> Callable:
        if iscoroutinefunction(func):
            return cast(Callable, partial(func, *args, **kwargs))
        else:

            async def f():
                return func(*args, **kwargs)

            return f


class PeriodicCall(TimedCall):
    """A TimedCall called at a fixed time intervals."""

    def start(self, interval: int | float, now: bool = True):  # type: ignore
        """Start calling the function periodically.

        :param interval: the time interval in seconds between calls.
        :param now: whether to make the first call immediately.

        """

        def times():
            time = self._loop.time()
            if not now:
                time += interval
            while True:
                yield time
                time += interval

        super().start(times())
