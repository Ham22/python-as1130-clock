import unittest
import clock
import time

class TestTime(unittest.TestCase):
    """ Test hardness to drive all LEDs """

    def setup(self):
        self.clock = clock.Clock()

    def test_past_the_hour(self):
        self.clock.updateTime() #TODO!

    def test_to_the_hour(self):
        self.clock.updateTime()

class TestHarness(unittest.TestCase):
    
    def setUp(self):
        self.clock = clock.Clock(animations_on=False)

    def test_run(self):
        for i in range(24):
             for j in range(60):
                 self.clock.updateTime(i, j)
                 time.sleep(0.001)


if __name__ == '__main__':
    unittest.main()
