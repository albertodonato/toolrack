import pytest

from ..periodic import (
    AlreadyRunning,
    NotRunning,
    PeriodicCall,
    TimedCall,
)


@pytest.fixture
def calls():
    yield []


@pytest.fixture
async def timed_call(calls):
    call = TimedCall(calls.append, True)
    yield call
    if call.running:
        await call.stop()


@pytest.fixture
def periodic_call(calls):
    yield PeriodicCall(calls.append, True)


@pytest.fixture
def time_intervals():
    return [1, 5]


@pytest.fixture
def times_iter(event_loop, time_intervals):
    def times():
        time = event_loop.time()
        for interval in time_intervals:
            time += interval
            yield time

    yield times


class TestTimedCall:
    def test_running(self, timed_call, times_iter):
        """The TimedCall is not running by default."""
        assert not timed_call.running
        timed_call.start(times_iter())
        assert timed_call.running

    @pytest.mark.asyncio
    async def test_start(self, advance_time, timed_call, times_iter, calls):
        """Starting the TimedCall makes it call the function."""
        timed_call.start(times_iter())
        await advance_time(2)
        assert calls == [True]

    def test_start_already_running(self, timed_call, times_iter):
        """Starting an already started TimedCall raises an error."""
        timed_call.start(times_iter())
        with pytest.raises(AlreadyRunning):
            timed_call.start(times_iter())

    @pytest.mark.asyncio
    async def test_stop(self, advance_time, timed_call, times_iter, calls):
        """Stopping the TimedCall stops runs."""
        timed_call.start(times_iter())
        await advance_time(2)
        await timed_call.stop()
        await advance_time(10)
        # Only the initial call is performed
        assert calls == [True]

    @pytest.mark.asyncio
    async def test_stop_not_running(self, timed_call):
        """Stopping a TimedCall that is not running raises an error."""
        with pytest.raises(NotRunning):
            await timed_call.stop()

    @pytest.mark.asyncio
    async def test_func_arguments(self, advance_time, times_iter, calls):
        """Specified arguments are passed to the function on call."""

        def func(*args, **kwargs):
            calls.append((args, kwargs))

        timed_call = TimedCall(func, "foo", "bar", baz="baz", bza="bza")
        timed_call.start(times_iter())
        await advance_time(2)
        await timed_call.stop()
        assert calls == [(("foo", "bar"), {"baz": "baz", "bza": "bza"})]

    def test_run_no_op_if_not_running(self, timed_call, times_iter, calls):
        """The _run() method no-ops if the Timedcall is not running."""
        timed_call._run(times_iter())
        assert calls == []

    @pytest.mark.asyncio
    async def test_run_at_time_intervals(
        self, timed_call, times_iter, time_intervals, calls
    ):
        """The function is called at specified time intervals."""
        time_intervals[:] = [5, 3]
        timed_call.start(times_iter())
        assert calls == []

    @pytest.mark.asyncio
    async def test_stop_after_iterator_ends(
        self, advance_time, timed_call, times_iter, time_intervals, calls
    ):
        """The TimedCall stops if the time iterator ends."""
        timed_call.start(times_iter())
        await advance_time(10)
        assert not timed_call.running
        assert calls == [True, True]


class TestPeriodicCall:
    @pytest.mark.asyncio
    async def test_start(self, advance_time, periodic_call, calls):
        """Starting the PeriodicCall makes it call the function immediately."""
        periodic_call.start(5)
        await advance_time(1)
        assert calls == [True]

    @pytest.mark.asyncio
    async def test_stop(
        self,
        advance_time,
        periodic_call,
        calls,
    ):
        """Stopping the PeriodicCall stops periodic runs."""
        periodic_call.start(5)
        await advance_time(1)
        await periodic_call.stop()
        await advance_time(10)
        # Only the initial call is performed
        assert calls == [True]

    @pytest.mark.asyncio
    async def test_periodic(self, advance_time, periodic_call, calls):
        """The PeriodicCall gets called at each interval."""
        periodic_call.start(5)
        await advance_time(6)
        assert calls == [True, True]
        await advance_time(5)
        assert calls == [True, True, True]

    @pytest.mark.asyncio
    async def test_start_later(self, advance_time, periodic_call, calls):
        """If now is False, the function is not run immediately."""
        periodic_call.start(5, now=False)
        await advance_time(1)
        assert calls == []

    @pytest.mark.asyncio
    async def test_start_later_run_after_interval(
        self, advance_time, periodic_call, calls
    ):
        """If now is False, the function is run after the interval."""
        periodic_call.start(5, now=False)
        await advance_time(6)
        assert calls == [True]
