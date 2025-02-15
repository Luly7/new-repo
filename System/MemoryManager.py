from hardware.Memory import Memory
from struct import unpack


class MemoryManager:
    def __init__(self, system, size):
        self.memory = Memory(size)
        self.system = system

    def prepare_program(self, filepath):
        """Validate program file and memory availability before loading."""

        if not filepath:
            return self.system_code(103, "Please specify the file path.")
                
        try:
            with open(filepath, 'rb') as f:
                # Unpack header, which consists of 3 integers (12 bytes)
                byte_size, pc, loader = self._read_header(f)
                
                if not self._is_valid_loader(loader, byte_size, filepath):
                    return None
                
                return {
                    'filepath': filepath,
                    'byte_size': byte_size,
                    'loader': loader,
                    'pc': pc,
                    'code_start': pc,
                    'code_end': loader + byte_size - 1,
                    'data_start': loader,
                    'data_end': pc - 1
                }

        except FileNotFoundError:
            print("File not found")
            self.system_code(109)
            return None
        except Exception as e:
            self.system_code(100)
            print("An error occurred while loading the file.")
            print(e)
            return None
        
    def _read_header(self, f):
        header = f.read(12)
        byte_size, pc, loader = unpack('III', header) 
        pc += loader
        return byte_size, pc, loader
    
    def _is_valid_loader(self, loader, byte_size, filepath):
        if loader > self.memory.size:
            self.system_code(110, f"Loader address {loader} is out of bounds.", filepath)
            return False
        
        if loader + byte_size > self.memory.size:
            self.system_code(102, f"Not enough memory to store program at location {loader}.\nProgram requires {byte_size} bytes.\nMemory has {self.memory.size - loader} bytes available.", filepath)
            return False
                
        return True
    
    def load_to_memory(self, pcb):

        # Check if another pcb is already loaded at the loader address and not terminated
        for other_pcb in self.system.ready_queue:
            if ((other_pcb != pcb and other_pcb['file'] != pcb['file']) and # Make sure it's not the same program
               (other_pcb['state'] not in ['TERMINATED', 'NEW'])): # Make sure it's not terminated or new
                if ((pcb['loader'] < other_pcb['code_end'] and pcb['loader'] > other_pcb['code_start']) or 
                   (pcb['code_end'] > other_pcb['loader'] and pcb['code_end'] < other_pcb['code_end'])):
                    self.system_code(102, pcb['file'])
                    return None
    
        with open(pcb['file'], 'rb') as f:
            f.seek(12) # Skip header
            self.memory[pcb['loader'] : pcb['loader'] + pcb['byte_size']] = f.read(pcb['byte_size'])

        self.system.print(self.memory)
        return True
    
    def release_resources(self, pcb):
        loader = pcb['loader']
        code_end = pcb['code_end']
        self.memory[loader:code_end+1] = [0] * (code_end - loader + 1)
        self.system.print(f"Released resources for {pcb}")

    def system_code(self, code, *args):
        self.system.system_code(code, *args)

    def check_memory_available(self, pcb):
        for existing_job in self.system.ready_queue:
            if ((pcb['loader'] < existing_job['code_end'] and pcb['loader'] + pcb['byte_size'] > existing_job['code_start']) or 
               (pcb['loader'] + pcb['byte_size'] > existing_job['code_start'] and pcb['loader'] < existing_job['code_end'])):
                # There is overlap in memory
                return False
        return True