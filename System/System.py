from hardware.Memory import Memory
from struct import unpack
from hardware.CPU import CPU
from hardware.Clock import Clock
from .PCB import PCB
from constants import USER_MODE, KERNEL_MODE, SYSTEM_CODES, instructions




# PCB = Process Control Block
# stores meta data for a process

class System:
    def __init__(self):
        self._memory = Memory('100B')
        self._CPU = CPU(self._memory, self)
        self._clock = Clock()
        self.mode = USER_MODE 
        self.loader = None
        self.verbose = False
        self.programs = {}
        self.errors = []
        self.system_codes = SYSTEM_CODES
        self.PCBs = {}

        # Process management queues
        self.ready_queue = []
        self.job_queue = []
        self.io_queue = []

    def switch_mode(self):
        new_mode = USER_MODE if self.mode == KERNEL_MODE else KERNEL_MODE
        if self.verbose: self.print(f"Switching user_mode from {self.mode} to {new_mode}")
        self.mode = new_mode

    def call(self, cmd, *args):
            
        commands = {
            'load': self.load_file,
            'coredump': self.coredump,
            'errordump': self.errordump,
            "run": self.run_progam, 
            "registers": lambda: print(self._CPU),
            "execute": self.execute,
        }

        if cmd in commands:
            try:
                self.switch_mode() # switch to kernel mode to execute the command
                self.print(f"Executing command: {cmd}")
                commands[cmd](*args) # look up the command in the dictionary and execute it
                self.switch_mode() # switch back to user mode after executing the command
                self.verbose = False # verbose is set to true in the shell, after running the cmd reset it
            except TypeError as e:
                self.system_code(103)
                print(e)
                print(f"Invalid arguments for command: {cmd}")
            except Exception as e:
                print(e)
                self.system_code(100)

        else:
            print(f"Unknown command: {cmd}")
            self.system_code(103)
        
    def execute(self, *args):
        if len(args) < 2:
            self.system_code(103)
            print("Please specify the program to execute and arrival time.")

        filepath = args[0]
        arrival_time = args[1]

        pcb = self.load_file(filepath, arrival_time)
        pcb.set_arrival_time(arrival_time)
        self.run_pcb(pcb)

    def load_file(self, filepath, arrival_time=0, *args):
        """ Load file into memory """
        if not filepath:
            return self._handle_error(103, "Please specify the file path.")
        
        if len(args) > 0:
            return self._handle_error(103, "load command only takes one argument, the file path.")
        
        try:
            with open(filepath, 'rb') as f:
                # Unpack header, which consists of 3 integers (12 bytes)
                byte_size, pc, loader = self._read_header(f)
                
                if not self._is_valid_loader(loader, byte_size):
                    self.system_codes(102)
                    return None
                
                pcb = self.createPCB(pc, filepath)
                self._load_instructions(f, pc, loader, byte_size, pcb)

                self.ready_queue.append(pcb)

                self.print("Program loaded at memory location {}".format(pcb['loader']))
                self.system_code(1)
                return pcb

        except FileNotFoundError:
            print("File not found")
            self.system_code(109)
            return None
        except Exception as e:
            self.system_code(100)
            print("An error occurred while loading the file.")
            print(e)
            return None
        
    def createPCB(self, pc, filepath):
        pid = len(self.PCBs) + 1
        registers = [0]*16
        state = 'NEW'
        pcb = PCB(pid, pc, registers, state)
        pcb['file'] = filepath 
        self.PCBs[filepath] = pcb
        return pcb
        
    def _handle_error(self, code, message):
        print(message)
        self.system_code(code)
        return None
    
    def _read_header(self, f):
        header = f.read(12)
        byte_size, pc, loader = unpack('III', header) 
        pc += loader
        self.print(f" - Loading program with {byte_size} bytes, PC at {pc}, loader at {loader}")
        return byte_size, pc, loader
    
    def _is_valid_loader(self, loader, byte_size):
        if loader > self._memory.size:
            self._handle_error(110, f"Loader address {loader} is out of bounds.")
            return False
        
        if loader + byte_size > self._memory.size:
            self._handle_error(102, f"Not enough memory to store program at location {loader}.\nProgram requires {byte_size} bytes.\nMemory has {self._memory.size - loader} bytes available.")
            return False
        
        if self._memory[loader] != 0 and self.loader is not None:
            self._handle_error(102, f"Memory location {loader} already contains a program.")
            return False
        
        return True
    
    def _load_instructions(self, f, pc, loader, byte_size, pcb):

        pcb['loader'] = loader
        # Load data section
        if (pc != loader):
            self.print(f" - Loading data section into memory starting at {loader}")
            pcb['data_start'] = loader
            while loader < pc:
                b = f.read(1)
                byte = unpack('B', b)[0]
                self._memory[loader] = byte
                loader += 1
            pcb['data_end'] = loader - 1
        else:
            pcb['data_start'] = pcb['data_end'] = None
            

        # Load code section
        pcb['code_start'] = loader
        while loader <= byte_size:
            instruction = f.read(6)
            self._memory[loader:loader+6] = instruction
            loader += 6
        pcb['code_end'] = loader - 1
    
        
    def run_pcb(self, pcb):
        if pcb['file'] not in self.PCBs:
            self.system_code(101)
            print(f"Program {pcb} not found.")
            return None
        
        self._CPU.run_program(pcb, self.verbose)

    def run_progam(self, *args):
        if len(self.PCBs) == 0:
            self.system_code(101)
            print("No program loaded.")
            return None
        
        if len(args) == 0:
            self.system_code(103)
            print("Please specify the program to run.")
            return None
        
        program = args[0]
        
        if program not in self.PCBs:
            self.system_code(101)
            print(f"Program {program} not found.")
            return None
        
        pcb = self.PCBs[program]

        self._CPU.run_program(pcb, self.verbose)
        self.loader = None



    def coredump(self):
        if self.verbose:
            print("Coredump:")
            print(self._memory)

        else:
            with open('memory.txt', 'w') as f:
                f.write(str(self._memory))
                # for i in range(self._memory.rows):
                #     f.write(str(self._memory[i]) + '\n')
            print("Memory dumped to memory.txt")
    
    def errordump(self):
        if self.verbose:
            print('Errors:')
            for error in self.errors:
                print(error)

        else:
            with open('errors.txt', 'w') as f:
                for error in self.errors:
                    f.write(str(error) + '\n')
            print("Errors dumped to errors.txt")    


    def print(self, txt):
        """ 
            Checks if system is in verbose mode,
            if so, print the message. 
        """
        if (self.verbose):
            print(txt)

    def log_error(self, code):
        if code not in self.system_codes:
            print(self.system_codes[100])
        
        if code >= 100:
            self.errors.append({
                'program': None,
                'code': code, 
                'message': self.system_codes[code]},
                )
        print(self.system_codes[code])

    def system_code(self, code):
        if code == 0 or code == 1:
            return None
        
        self.log_error(code)

if __name__ == '__main__':
    system = System()
    print(system.mode)
    system.switch_mode()
    print(system.mode)
    system.switch_mode()
    print(system.mode)