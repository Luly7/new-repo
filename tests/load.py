import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from System import System

if __name__ == '__main__':
    system = System()
    system.verbose = True
    system.load_file('test2.osx')
    system.verbose = True
    system.call('run', 'test2.osx')
    system.verbose = True
    system.call('coredump')
    system.verbose = True
    system.call('registers')
    
