from hardware.Memory import Memory
from struct import unpack
from hardware.CPU import CPU
from system_codes import SYSTEM_CODES

USER_MODE = 0x01
KERNEL_MODE = 0x00



# PCB = Process Control Block
# stores meta data for a process

class System:
    def __init__(self):
        self._memory = Memory('100B')
        self._CPU = CPU(self._memory, self)
        self.mode = self._memory[0][0]
        self.loader = None
        self.verbose = False
        self.programs = {}
        self.errors = []
        self.system_codes = SYSTEM_CODES

    def switch_mode(self):
        newMode = USER_MODE if self.mode == KERNEL_MODE else KERNEL_MODE
        if self.verbose: self.print(f"Switching user_mode from {self.mode} to {newMode}")
        self._memory[0][0] = newMode
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
        
        

    def load_file(self, filepath, *args):
        """ Load file into memory """
        if not filepath:
            print("Please specify the file path.")
            self.system_code(103)
            return None
        
        if len(args) > 0:
            print("load command only takes one argument, the file path.")
            self.system_code(103)
            return None
        
        try:
            with open(filepath, 'rb') as f:
                # Unpack header, which consists of 3 integers (12 bytes)
                header = f.read(12)
                byteSize, pc, loader = unpack('III', header) 
                self.print(f" - Loading program with {byteSize} bytes, PC at {pc}, loader at {loader}")
                lines = byteSize // 6

                # Check if loader is out of bounds
                if loader > self._memory.rows:
                    print(f"Memory location {loader} is out of bounds.\n") + \
                    (f"Memory has {self._memory.rows} lines available.")
                    self.system_code(110)
                
                # Check if there is enough memory to store the program
                if loader + lines > self._memory.rows:
                    print(f"Not enough memory to store program at location {loader}.")
                    print(f"Program requires memory to have {lines} lines available.")
                    print(f"Memory has {self._memory.rows - loader} lines available.")
                    self.system_code(102)

                # Check if there is already a program loaded at the loader location
                if self._memory[loader][0] != 0 and self.loader is not None:
                    print(f"Memory location {loader} already contains a program.")
                    self.system_code(102)
                
                self.loader = loader

                self.programs[filepath] = {'program': filepath, 'start': loader, 'end': loader + lines}
                
                # Load program into memory
                i = loader

                while True:
                    chunk = f.read(6) # There are 6 bytes per instruction
                    if not chunk: # end of file
                        break

                    if (len(chunk) < 6):
                        print('incomplete instruction found, terminating', chunk)
                        self.system_code(103)
                        break # skip incomplete instructions

                    values = unpack('6B', chunk)
                    self.print(f" - Loading values {values} into memory location {i}")


                    for j in range(6):
                        self._memory[i][j] = values[j] if values[j] != 32 else 0 # 32 is the ASCII code for space
                    i += 1
                
                print(f"Program loaded at memory location {loader}")
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
        
    def run_progam(self, *args):
        if self.loader is None:
            self.system_code(101)
            print("No program loaded.")
            return None
        
        if len(args) == 0:
            self.system_code(103)
            print("Please specify the program to run.")
            return None
        
        program = args[0]
        
        pcb = self.programs[program]

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