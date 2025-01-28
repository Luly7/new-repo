import unittest

from Clock import Clock

class TestClock(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
    
    def test_print(self):
        self.assertEqual(str(self.clock), "0")

    def test_increment(self):
        self.clock.increment()
        self.assertEqual(str(self.clock), "1")

    def test_iadd(self):
        self.clock += 5
        self.assertEqual(str(self.clock), "5")


if __name__ == '__main__':
    unittest.main()