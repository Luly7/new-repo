import sys
import struct
from hardware.Memory import Memory
from System.PCB import PCB
from System.System import System



def load_osx(filepath):
    memory = Memory('100B')
    pcb = PCB(1, 0, [0] * 8, 'NEW')


    running = True
    if running:
        with open(filepath, 'rb') as f:

            header = f.read(12)
            byteSize, pc, loader = struct.unpack('III', header)


            # Load data section
            if (pc != loader):
                pcb.data_start = loader
                while loader <= pc:
                    b = f.read(1)
                    byte = struct.unpack('B', b)[0]
                    memory[loader] = byte
                    loader += 1
                pcb.data_end = loader - 1
            else:
                pcb.data_start = pcb.data_end = None


            # Load code section
            pcb.code_start = loader
            while loader <= byteSize:
                b = f.read(1)
                byte = struct.unpack('B', b)[0]
                memory[loader] = byte
                loader += 1
            pcb.code_end = loader - 1
            
            print()
            print(memory)
            print(memory[pcb.code_start], memory[pcb.code_end+1])
            if pcb.data_start is not None and pcb.data_end is not None:
                data_section = memory[pcb.data_start:pcb.data_end+1]
                data_integers = struct.unpack(f'{len(data_section)}B', bytes(data_section))
                print(data_integers)
            code_section = memory[pcb.code_start:pcb.code_end+1]
            code_integers = struct.unpack(f'{len(code_section)}B', bytes(code_section))
            print(code_integers)
        
system = System()
def load_into_system(filepath):
    global system
    return system.load_file(filepath)

def run_pcb(pcb):
    global system
    system.run_pcb(pcb)

def main():
    if (len(sys.argv) == 2):
        filepath = sys.argv[1]
    else:
        filepath = 'test2.osx'
    pcb = load_into_system(filepath)
    print(system._memory)
    run_pcb(pcb)

if __name__ == "__main__":
    main()
