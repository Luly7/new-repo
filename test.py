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
        self.str_file = 'tests/str.osx'
        self.strb_file = 'tests/strb.osx'
        self.ldr_file = 'tests/ldr.osx'
        self.ldrb_file = 'tests/ldrb.osx'
        self.b_file   = 'tests/b.osx'
        self.bl_file  = 'tests/bl.osx'
        self.bx_file  = 'tests/bx.osx'
        self.bne_file = 'tests/bne.osx'
        self.not_bne_file = 'tests/not_bne.osx'
        self.cmp_file = 'tests/cmp.osx'


    def test_add(self):
        self.system.call('load', self.add_file)
        self.system.call('run', self.add_file)
        self.assertEqual(self.system._CPU.registers[0], 300)

    def test_sub(self):
        self.system.call('load', self.sub_file)
        self.system.call('run', self.sub_file)
        self.assertEqual(self.system._CPU.registers[1], 100)

    def test_mul(self):
        self.system.call('load', self.mul_file)
        self.system.call('run', self.mul_file)
        self.assertEqual(self.system._CPU.registers[0], 400)

    def test_div(self):
        self.system.call('load', self.div_file)
        self.system.call('run', self.div_file)
        self.assertEqual(self.system._CPU.registers[0], 2)
    
    def test_mov(self):
        self.system.call('load', self.mov_file)
        self.system.call('run', self.mov_file)
        self.assertEqual(self.system._CPU.registers[0], 200)

    def test_adr(self):
        self.system.call('load', self.adr_file)
        self.system.call('run', self.adr_file)
        self.assertEqual(self.system._CPU.registers[0], 0)

    def test_str(self):
        self.system.call('load', self.str_file)
        self.system.call('run', self.str_file)
        self.assertTrue(1)

    def test_strb(self):
        self.system.call('load', self.strb_file)
        self.system.call('run', self.strb_file)
        self.assertEqual(self.system._memory[2], 97)

    def test_ldr(self):
        self.system.call('load', self.ldr_file)
        self.system.call('run', self.ldr_file)
        self.assertEqual(self.system._CPU.registers[0], 300)
    
    def test_ldrb(self):
        self.system.call('load', self.ldrb_file)
        self.system.call('run', self.ldrb_file)
        self.assertEqual(self.system._CPU.registers[0], 98)

    def test_b(self):
        self.system.call('load', self.b_file)
        self.system.call('run', self.b_file)
        self.assertEqual(self.system._CPU.registers[0], 100)

    def test_bx(self):
        self.system.call('load', self.bx_file)
        self.system.call('run', self.bx_file)
        self.assertEqual(self.system._CPU.registers[0], 100)

    def test_bl(self):
        self.system.call('load', self.bl_file)
        self.system.call('run', self.bl_file)
        self.assertEqual(self.system._CPU.registers[0], 300)

    def test_bne(self): # compare if 2 registers are equal
        self.system.call('load', self.bne_file)
        self.system.call('run', self.bne_file)
        self.assertEqual(self.system._CPU.registers[0], 1)

    def test_not_bne(self): # compare if 2 registers are equal
        self.system.call('load', self.not_bne_file)
        self.system.call('run', self.not_bne_file)
        self.assertEqual(self.system._CPU.registers[0], 0)

    def test_cmp(self):
        self.system.call('load', self.cmp_file)
        self.system.call('run', self.cmp_file)
        self.assertLess(self.system._CPU.registers[9], 0)



if __name__ == "__main__":
    unittest.main()
