#!/usr/bin/python3

import unittest

import time

from as1130_led_grid import AS1130LedGrid
from clock import Clock


class TestHarness(unittest.TestCase):

    def test_run(self):
        self.clock = Clock(AS1130LedGrid(0, 0x30), animations_on=False)
        for i in range(24):
            for j in range(60):
                self.clock.update_time(i, j)
                time.sleep(0.1)


if __name__ == '__main__':
    unittest.main()
