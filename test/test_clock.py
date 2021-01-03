#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock, call

from clock import clock


class TestClock(unittest.TestCase):

    def setUp(self):
        self.grid = MagicMock()
        self.clock = clock.Clock(self.grid)

    def test_grid_is_cleared_before_setting_new_led(self):
        self.clock.update_time(1, 26)

        calls = [call.clear(), call.set_led(0, 0)]
        self.grid.assert_has_calls(calls, any_order=False)

    def test_fades_out_before_clearing(self):
        self.clock.update_time(1, 26)

        calls = [call.fade_out(), call.clear(), call.set_led(0, 0)]
        self.grid.assert_has_calls(calls, any_order=False)

    def test_fades_in_after_setting_last_led(self):
        self.clock.update_time(1, 26)

        calls = [call.set_led(3, 4), call.fade_in()]
        self.grid.assert_has_calls(calls, any_order=False)

    def test_fade_can_be_disabled(self):
        self.clock = clock.Clock(self.grid, animations_on=False)

        self.clock.update_time(1, 26)

        self.grid.fade_out.assert_not_called()
        self.grid.fade_in.assert_not_called()


if __name__ == '__main__':
    unittest.main()
