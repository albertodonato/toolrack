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

from ..testing.async import LoopTestCase
from ..async import PeriodicCall


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
