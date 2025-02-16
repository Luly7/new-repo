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
        file1 = os.path.join(os.path.dirname(__file__), 'programs\load_test_1.osx')
        file2 = os.path.join(os.path.dirname(__file__), 'programs\load_test_2.osx')

        self.system.call('execute', file1, 0, file2, 2)
        
        pcb1 = None
        pcb2 = None
        for file in self.system.terminated_queue:
            if file.file == file1:
                pcb1 = file
            if file.file == file2:
                pcb2 = file

        self.assertEqual(pcb1.arrival_time, 0)
        self.assertEqual(pcb1.waiting_time, 0)
        self.assertEqual(pcb2.arrival_time, 2)
        self.assertEqual(pcb2.waiting_time, 1)




if __name__ == "__main__":
    unittest.main()