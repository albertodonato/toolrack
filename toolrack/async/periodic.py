"""Utilities based on the asyncio library.

This modules provides a :class:`PeriodicCall` class to periodically execute a
task.

"""

from asyncio import Future


class AlreadyRunning(Exception):
    """The :class:`PeriodicCall` is already running."""

    def __init__(self):
        super().__init__('PeriodicCall is already running')


class NotRunning(Exception):
    """The :class:`PeriodicCall` is not running."""

    def __init__(self):
        super().__init__('PeriodicCall is not running')


class PeriodicCall:
    """Call a function at a periodic interval.

    The class takes a function with optional arguments. Upon
    :meth:`start()`, the function is scheduled with the specified interval,
    until :meth:`stop()` is called.

    :param loop: the event loop to use.
    :param callable func: the function to call periodically.
    :param list args: arguments to pass to the function.
    :param dict kwargs: keyword arguments to pass to the function.

    """

    def __init__(self, loop, func, *args, **kwargs):
        self._loop = loop
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._interval = None
        self._next_time = None
        self._future = None

    @property
    def running(self):
        """Whether the PeriodicCall is currently running."""
        return self._future is not None

    def start(self, interval, now=True):
        """Start calling the function periodically.

        :param interval: the time interval in seconds between calls.
        :param bool now: whether to make the first call immediately.

        """
        if self.running:
            raise AlreadyRunning()

        self._interval = interval
        self._next_time = self._loop.time()
        self._future = Future()
        self._run(now=now)

    async def stop(self):
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

    def _run(self, now=True):
        if not self.running:
            return

        self._next_time += self._interval
        self._handle = self._loop.call_at(self._next_time, self._run)
        if now:
            self._func(*self._args, **self._kwargs)
