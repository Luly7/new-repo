import unittest
import sys
from System.System import System

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.system = System()
        self.add_file = 'tests/add.osx'
        self.sub_file = 'tests/sub.osx'
        self.mul_file = 'tests/mul.osx'
        self.div_file = 'tests/div.osx'
        self.mov_file = 'tests/mov.osx'
        self.adr_file = 'tests/adr.osx'

    # def test_add(self):
    #     self.system.call('load', self.add_file)
    #     self.system.call('run', self.add_file)
    #     self.assertEqual(self.system._CPU.registers[0], 300)

    # def test_sub(self):
    #     self.system.call('load', self.sub_file)
    #     self.system.call('run', self.sub_file)
    #     self.assertEqual(self.system._CPU.registers[1], 100)

    # def test_mul(self):
    #     self.system.call('load', self.mul_file)
    #     self.system.call('run', self.mul_file)
    #     self.assertEqual(self.system._CPU.registers[0], 400)

    # def test_div(self):
    #     self.system.call('load', self.div_file)
    #     self.system.call('run', self.div_file)
    #     self.assertEqual(self.system._CPU.registers[0], 2)
    
    # def test_mov(self):
    #     self.system.call('load', self.mov_file)
    #     self.system.call('run', self.mov_file)
    #     self.assertEqual(self.system._CPU.registers[0], 200)

    def test_adr(self):
        self.system.call('load', self.adr_file)
        self.system.call('run', self.adr_file)
        self.assertEqual(self.system._CPU.registers[0], 0)

        
def load_into_system(system, filepath):
    return system.load_file(filepath)

def run_pcb(system, pcb):
    system.run_pcb(pcb)

def get_registers(system):
    return system._CPU.registers

def main():
    system = System()
    if (len(sys.argv) == 2):
        filepath = sys.argv[1]
    else:
        filepath = 'tests/mov.osx'
    pcb = load_into_system(system, filepath)
    run_pcb(system, pcb)
    

    assert get_registers(system)[0] == 200

if __name__ == "__main__":
    unittest.main()
    # main()
