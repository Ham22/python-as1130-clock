#!/usr/bin/python3

import unittest

import time

import clock


class TestHarness(unittest.TestCase):

    def test_run(self):
        self.clock = clock.Clock(animations_on=False)
        for i in range(24):
             for j in range(60):
                 self.clock.update_time(i, j)
                 time.sleep(0.001)


if __name__ == '__main__':
    unittest.main()
