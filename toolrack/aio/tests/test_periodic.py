import pytest

from ..periodic import (
    AlreadyRunning,
    NotRunning,
    PeriodicCall,
)


@pytest.fixture
def calls():
    yield []


@pytest.fixture
def periodic_call(event_loop, calls):
    yield PeriodicCall(event_loop, calls.append, True)


class TestPeriodicCall:
    def test_running(self, periodic_call):
        """The PeriodicCall is not running by default."""
        assert not periodic_call.running
        periodic_call.start(5)
        assert periodic_call.running

    def test_start(self, periodic_call, calls):
        """Starting the PeriodicCall makes it call the function immediately."""
        periodic_call.start(5)
        assert calls == [True]

    def test_start_already_running(self, periodic_call):
        """Starting an already started PeriodicCall raises an error."""
        periodic_call.start(5)
        with pytest.raises(AlreadyRunning):
            periodic_call.start(5)

    @pytest.mark.asyncio
    async def test_stop(
        self, advance_time, periodic_call, calls,
    ):
        """Stopping the PeriodicCall stops periodic runs."""
        periodic_call.start(5)
        await periodic_call.stop()
        await advance_time(5)
        # Only the initial call is performed
        assert calls == [True]

    @pytest.mark.asyncio
    async def test_stop_not_running(self, periodic_call):
        """Stopping a PeriodicCall that is not running raises an error."""
        with pytest.raises(NotRunning):
            await periodic_call.stop()

    @pytest.mark.asyncio
    async def test_periodic(self, advance_time, periodic_call, calls):
        """The PeriodicCall gets called at each interval."""
        periodic_call.start(5)
        await advance_time(5)
        assert calls == [True, True]
        await advance_time(5)
        assert calls == [True, True, True]

    def test_start_later(self, periodic_call, calls):
        """If now is False, the function is not run immediately."""
        periodic_call.start(5, now=False)
        assert calls == []

    @pytest.mark.asyncio
    async def test_start_later_run_after_interval(
        self, advance_time, periodic_call, calls
    ):
        """If now is False, the function is run after the interval."""
        periodic_call.start(5, now=False)
        await advance_time(5)
        assert calls == [True]

    @pytest.mark.asyncio
    async def test_func_arguments(self, event_loop, calls):
        """Specified arguments are passed to the function on call."""

        def func(*args, **kwargs):
            calls.append((args, kwargs))

        periodic_call = PeriodicCall(
            event_loop, func, "foo", "bar", baz="baz", bza="bza"
        )
        periodic_call.start(5)
        await periodic_call.stop()
        assert calls == [(("foo", "bar"), {"baz": "baz", "bza": "bza"})]

    def test_run_no_op_if_not_running(self, periodic_call, calls):
        """The _run() method no-ops if the PeriodicCall is not running."""
        periodic_call._run()
        assert calls == []
