from hardware.Memory import Memory
from struct import unpack
from hardware.CPU import CPU
from hardware.Clock import Clock
from . import PCB
from constants import USER_MODE, KERNEL_MODE, SYSTEM_CODES, instructions




# PCB = Process Control Block
# stores meta data for a process

class System:
    def __init__(self):
        self._memory = Memory('100B')
        self._CPU = CPU(self._memory, self)
        self._clock = Clock()
        self.mode = self._memory[0][0]
        self.loader = None
        self.verbose = False
        self.programs = {}
        self.errors = []
        self.system_codes = SYSTEM_CODES
        self.PCBs = {}

    def switch_mode(self):
        new_mode = USER_MODE if self.mode == KERNEL_MODE else KERNEL_MODE
        if self.verbose: self.print(f"Switching user_mode from {self.mode} to {new_mode}")
        self._memory[0][0] = new_mode
        self.mode = self._memory[0][0]

    def call(self, cmd, *args):
            
        commands = {
            'load': self.load_file,
            'coredump': self.coredump,
            'errordump': self.errordump,
            "run": self.run_progam, 
            "registers": lambda: print(self._CPU)
        }

        if cmd in commands:
            try:
                self.switch_mode() # switch to kernel mode to execute the command
                self.print(f"Executing command: {cmd}")
                commands[cmd](*args) # look up the command in the dictionary and execute it
                self.switch_mode() # switch back to user mode after executing the command
                self.verbose = False # verbose is set to true in the shell, after running the cmd reset it
            except TypeError:
                self.system_code(103)
                print(f"Invalid arguments for command: {cmd}")
            except Exception as e:
                print(e)
                self.system_code(100)

        else:
            print(f"Unknown command: {cmd}")
            self.system_code(103)
        
        
    def _handle_error(self, code, message):
        print(message)
        self.system_code(code)
        return None
    
    def _read_header(self, f):
        header = f.read(12)
        byte_size, pc, loader = unpack('III', header) 
        self.print(f" - Loading program with {byte_size} bytes, PC at {pc}, loader at {loader}")
        lines = byte_size // 6
        return byte_size, pc, loader, lines
    
    def _is_valid_loader(self, loader, lines):
        if loader > self._memory.rows:
            self._handle_error(110, f"Memory location {loader} is out of bounds.\nMemory has {self._memory.rows} lines available.")
            return False
        
        if loader + lines > self._memory.rows:
            self._handle_error(102, f"Not enough memory to store program at location {loader}.\nProgram requires memory to have {lines} lines available.\nMemory has {self._memory.rows - loader} lines available.")
            return False
        
        if self._memory[loader][0] != 0 and self.loader is not None:
            self._handle_error(102, f"Memory location {loader} already contains a program.")
            return False
        
        return True
    
    def _load_instructions(self, f, loader):
        while True:
            opcode_byte = f.read(1)
            if not opcode_byte: # end of file
                break

            opcode_number = unpack('B', opcode_byte)[0]
            opcode_instruction = instructions[opcode_number]
            if (opcode_instruction in ['ADD', 'SUB', 'MUL', 'DIV']): # 2 Unused bytes
                self.load_instruction(f, opcode_byte, loader, opcode_instruction, 3)

            elif (opcode_instruction in ['MOV', 'STR', 'STRB', 'LDR', 'LDRB', 'CMP', 'AND', 'ORR', 'EOR']):
                self.load_instruction(f, opcode_byte, loader, opcode_instruction, 2)

            elif (opcode_instruction in ['MVI', 'ADR']):
                self.load_instruction(f, opcode_byte, loader, opcode_instruction, 5)

            elif (opcode_instruction in ['B', 'BL', 'BNE', 'BGT', 'BLT', 'BEQ', 'SWI']):
                self.load_instruction(f, opcode_byte, loader, opcode_instruction, 4)

            elif opcode_instruction in ['BX']:
                self.load_instruction(f, opcode_byte, loader, opcode_instruction, 1)

            else:
                self._memory[loader][0] = opcode_byte
                for i in range(1,5):
                    byte = f.read(1)
                    if not byte:
                        break
                    self._memory[loader][i] = unpack('B', byte)[0]
            
            loader += 1
    
    def load_file(self, filepath, *args):
        """ Load file into memory """
        if not filepath:
            return self._handle_error(103, "Please specify the file path.")
        
        if len(args) > 0:
            return self._handle_error(103, "load command only takes one argument, the file path.")
        
        try:
            with open(filepath, 'rb') as f:
                # Unpack header, which consists of 3 integers (12 bytes)
                byte_size, pc, loader, lines = self._read_header(f)
                
                if not self._is_valid_loader(loader, lines):
                    return None
                
                self.loader = loader

                self.programs[filepath] = {'program': filepath, 'start': loader, 'end': loader + lines}

                self._load_instructions(f, loader)
                
                pid = len(self.PCBs) + 1
                registers = [0]*16
                state = 'READY'
                pcb = PCB(pid, pc, registers, state)
                self.PCBs[filepath] = pcb

                print("Program loaded at memory location {}".format(self.programs[filepath]['start']))
                self.system_code(1)

        except FileNotFoundError:
            print("File not found")
            self.system_code(109)
            return None
        except Exception as e:
            self.system_code(100)
            print("An error occurred while loading the file.")
            print(e)
            return None
        
    def load_instruction(self, f, opcode_byte, loader, instruction, byte_count):
        opcode_byte += f.read(byte_count)
        op = unpack(f'{byte_count+1}B', opcode_byte)
        self.print(f" - Loading instruction {instruction} with values {op} into memory location {loader}")
        for i in range(byte_count+1):
            self._memory[loader][i] = op[i]
        f.read(5 - byte_count)
        
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
            for i in range(self._memory.rows):
                print(self._memory[i])

        else:
            with open('memory.txt', 'w') as f:
                for i in range(self._memory.rows):
                    f.write(str(self._memory[i]) + '\n')
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