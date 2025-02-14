import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from System.System import System

class TestLoadFunction(unittest.TestCase):
    def setUp(self):
        self.system = System()
        return super().setUp()

    def test_load_function(self):
        file1 = 'programs/add.osx'
        self.system.handle_load(file1)

        self.assertEqual(len(self.system.job_queue), 1)
        self.assertEqual(self.system.job_queue[0].file, file1)





if __name__ == "__main__":
    unittest.main()