import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from System.System import System

class TestLoadFunction(unittest.TestCase):
    def setUp(self):
        self.system = System()
        self.file = 'tests/ops/add.osx'
        self.system.handle_load(self.file)

        return super().setUp()

    def test_load_function(self):
        self.system.run_program(self.file)

        self.assertEqual(self.system.CPU.registers[0], 300)





if __name__ == "__main__":
    unittest.main()