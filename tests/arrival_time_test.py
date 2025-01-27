import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from System.System import System

class TestArrivalTime(unittest.TestCase):
    def setUp(self):
        self.system = System()
        return super().setUp()

    def test_set_arrival_time(self):
        file1 = 'test.osx'
        file2 = 'test2.osx'
        self.system.call('execute', file1, 0, file2, 2)
        
        self.assertEqual(self.system.PCBs[file1].arrival_time, 0)
        self.assertEqual(self.system.PCBs[file1].waiting_time, 0)
        self.assertEqual(self.system.PCBs[file2].arrival_time, 2)
        self.assertEqual(self.system.PCBs[file2].waiting_time, 1)




if __name__ == "__main__":
    unittest.main()