#!/usr/bin/python3

import unittest

import clock


class TestTime(unittest.TestCase):
    """ Test hardness to drive all LEDs """

    def setup(self):
        self.clock = clock.Clock()

    def test_past_the_hour(self):
        self.clock.update_time() #TODO!

    def test_to_the_hour(self):
        self.clock.update_time()


if __name__ == '__main__':
    unittest.main()
