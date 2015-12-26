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

'''Asynchronous execution utils.'''

from asyncio import Future


class AlreadyRunning(Exception):
    '''The PeriodicCall is already running.'''

    def __init__(self):
        super().__init__('PeriodicCall is already running')


class NotRunning(Exception):
    '''The PeriodicCall is not running.'''

    def __init__(self):
        super().__init__('PeriodicCall is not running')


class PeriodicCall:
    '''Call a function at a periodic interval.

    Parameters:
        - loop: the event loop to use.
        - func: the function to call periodically.
        - args: arguments to pass to the function.

    '''

    def __init__(self, loop, func, *args):
        self._loop = loop
        self._func = func
        self._args = args
        self._interval = None
        self._next_time = None
        self._future = None

    @property
    def running(self):
        '''Whether the PeriodicCall is currently running.'''
        return self._future is not None

    def start(self, interval, now=True):
        '''Start calling the function periodically.'''
        if self.running:
            raise AlreadyRunning()

        self._interval = interval
        self._next_time = self._loop.time()
        self._future = Future()
        self._run(now=now)

    async def stop(self):
        '''Stop calling the function periodically.

        It returns an :class:`asyncio.Future` to wait for the stop to complete.

        '''
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
            self._func(*self._args)
