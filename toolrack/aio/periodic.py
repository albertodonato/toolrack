"""Utilities based on the asyncio library.

This modules provides :class:`TimedCall` and :class:`PeriodicCall` classes for
timed and periodical tasks execution.

"""

from asyncio import (
    Future,
    get_event_loop,
)
from typing import (
    Callable,
    Iterable,
    Optional,
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


TimesIterable = Iterable[Union[float, int]]


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
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._next_time = None
        self._future: Optional[Future] = None
        self._loop = get_event_loop()

    @property
    def running(self):
        """Whether the PeriodicCall is currently running."""
        return self._future is not None

    def start(self, times_iter: TimesIterable):
        """Start calling the function at specified times.

        :param times_iter: an iterable yielding times to execute the function
        at. If the iterator exhausts, the TimedCall is stopped.  Times must be
        compatible with :meth:`loop.time()`.

        """
        if self.running:
            raise AlreadyRunning()

        self._future = Future()
        self._run(times_iter, do_call=False)

    def stop(self):
        """Stop calling the function periodically.

        It returns an :class:`asyncio.Future` to wait for the stop to complete.

        """
        if not self.running:
            raise NotRunning()

        self._handle.cancel()
        self._handle = None

        future, self._future = self._future, None
        future.set_result(None)
        return future

    def _run(self, times_iter: TimesIterable, do_call: bool = True):
        if not self.running:
            return

        now = self._loop.time()
        next_time: Union[float, int] = -1
        while next_time < now:
            try:
                next_time = next(times_iter)  # type: ignore
            except StopIteration:
                self.stop()
                break

        if self.running:
            self._handle = self._loop.call_at(next_time, self._run, times_iter)
        if do_call:
            self._func(*self._args, **self._kwargs)


class PeriodicCall(TimedCall):
    """A TimedCall called at a fixed time intervals."""

    def start(self, interval: Union[int, float], now: bool = True):  # type: ignore
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
