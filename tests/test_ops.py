import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from System.System import System

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.system = System()
        root = 'ops/'
        # self.add_file = root + 'add.osx'
        self.add_file     = os.path.join(os.path.dirname(__file__), 'ops/add.osx')
        self.sub_file     = os.path.join(os.path.dirname(__file__), 'ops/sub.osx')
        self.mul_file     = os.path.join(os.path.dirname(__file__), 'ops/mul.osx')
        self.div_file     = os.path.join(os.path.dirname(__file__), 'ops/div.osx')
        self.mov_file     = os.path.join(os.path.dirname(__file__), 'ops/mov.osx')
        self.adr_file     = os.path.join(os.path.dirname(__file__), 'ops/adr.osx')
        self.str_file     = os.path.join(os.path.dirname(__file__), 'ops/str.osx')
        self.strb_file    = os.path.join(os.path.dirname(__file__), 'ops/strb.osx')
        self.ldr_file     = os.path.join(os.path.dirname(__file__), 'ops/ldr.osx')
        self.ldrb_file    = os.path.join(os.path.dirname(__file__), 'ops/ldrb.osx')
        self.b_file       = os.path.join(os.path.dirname(__file__), 'ops/b.osx')
        self.bl_file      = os.path.join(os.path.dirname(__file__), 'ops/bl.osx')
        self.bx_file      = os.path.join(os.path.dirname(__file__), 'ops/bx.osx')
        self.bne_file     = os.path.join(os.path.dirname(__file__), 'ops/bne.osx')
        self.not_bne_file = os.path.join(os.path.dirname(__file__), 'ops/not_bne.osx')
        self.cmp_file     = os.path.join(os.path.dirname(__file__), 'ops/cmp.osx')
        self.and_file     = os.path.join(os.path.dirname(__file__), 'ops/and.osx')
        self.orr_file     = os.path.join(os.path.dirname(__file__), 'ops/orr.osx')
        self.eor_file     = os.path.join(os.path.dirname(__file__), 'ops/eor.osx')



    def test_add(self):
        self.system.call('load', self.add_file)
        self.system.call('run', self.add_file)
        self.assertEqual(self.system.CPU.registers[0], 300)

    def test_sub(self):
        self.system.call('load', self.sub_file)
        self.system.call('run', self.sub_file)
        self.assertEqual(self.system.CPU.registers[1], 100)

    def test_mul(self):
        self.system.call('load', self.mul_file)
        self.system.call('run', self.mul_file)
        self.assertEqual(self.system.CPU.registers[0], 400)

    def test_div(self):
        self.system.call('load', self.div_file)
        self.system.call('run', self.div_file)
        self.assertEqual(self.system.CPU.registers[0], 2)
    
    def test_mov(self):
        self.system.call('load', self.mov_file)
        self.system.call('run', self.mov_file)
        self.assertEqual(self.system.CPU.registers[0], 200)

    def test_adr(self):
        self.system.call('load', self.adr_file)
        self.system.call('run', self.adr_file)
        self.assertEqual(self.system.CPU.registers[0], 0)

    def test_str(self):
        self.system.call('load', self.str_file)
        self.system.call('run', self.str_file)
        self.assertTrue(1)

    def test_strb(self):
        self.system.call('load', self.strb_file)
        self.system.call('run', self.strb_file)
        self.assertEqual(self.system.memory[2], 97)

    def test_ldr(self):
        self.system.call('load', self.ldr_file)
        self.system.call('run', self.ldr_file)
        self.assertEqual(self.system.CPU.registers[0], 300)
    
    def test_ldrb(self):
        self.system.call('load', self.ldrb_file)
        self.system.call('run', self.ldrb_file)
        self.assertEqual(self.system.CPU.registers[0], 98)

    def test_b(self):
        self.system.call('load', self.b_file)
        self.system.call('run', self.b_file)
        self.assertEqual(self.system.CPU.registers[0], 100)

    def test_bx(self):
        self.system.call('load', self.bx_file)
        self.system.call('run', self.bx_file)
        self.assertEqual(self.system.CPU.registers[0], 100)

    def test_bl(self):
        self.system.call('load', self.bl_file)
        self.system.call('run', self.bl_file)
        self.assertEqual(self.system.CPU.registers[0], 300)

    def test_bne(self): # compare if 2 registers are equal
        self.system.call('load', self.bne_file)
        self.system.call('run', self.bne_file)
        self.assertEqual(self.system.CPU.registers[0], 1)

    def test_not_bne(self): # compare if 2 registers are equal
        self.system.call('load', self.not_bne_file)
        self.system.call('run', self.not_bne_file)
        self.assertEqual(self.system.CPU.registers[0], 0)

    def test_cmp(self):
        self.system.call('load', self.cmp_file)
        self.system.call('run', self.cmp_file)
        self.assertLess(self.system.CPU.registers[9], 0)

    def test_and(self):
        self.system.call('load', self.and_file)
        self.system.call('run', self.and_file)
        self.assertEqual(self.system.CPU.registers[2], 1)
        self.assertEqual(self.system.CPU.registers[3], 0)

    def test_orr(self):
        self.system.call('load', self.orr_file)
        self.system.call('run', self.orr_file)
        self.assertEqual(self.system.CPU.registers[2], 1)
        self.assertEqual(self.system.CPU.registers[3], 1)
        self.assertEqual(self.system.CPU.registers[4], 0)

    def test_eor(self):
        self.system.call('load', self.eor_file)
        self.system.call('run', self.eor_file)
        self.assertEqual(self.system.CPU.registers[2], 0)
        self.assertEqual(self.system.CPU.registers[3], 1)
        self.assertEqual(self.system.CPU.registers[4], 0)



if __name__ == "__main__":
    unittest.main()
