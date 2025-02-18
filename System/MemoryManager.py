from hardware.Memory import Memory
from struct import unpack


class MemoryManager:
    def __init__(self, system, size):
        self.memory = Memory(size)
        self.system = system
        self.memory_map = []

    def prepare_program(self, filepath):
        """ Prepare program for loading into memory. """

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
        """ Read the header of the program file. """
        header = f.read(12)
        byte_size, pc, loader = unpack('III', header) 
        pc += loader
        return byte_size, pc, loader
    
    def _is_valid_loader(self, loader, byte_size, filepath):
        """ Check if loader address is valid. """
        if loader > self.memory.size:
            self.system_code(110, f"Loader address {loader} is out of bounds.", filepath)
            return False
        
        if loader + byte_size > self.memory.size:
            self.system_code(102, f"Not enough memory to store program at location {loader}.\nProgram requires {byte_size} bytes.\nMemory has {self.memory.size - loader} bytes available.", filepath)
            return False
                
        return True
    
    def allocate_memory(self, pcb):
        """ Allocate memory if available and update memory map. """
        end = pcb.loader + pcb.byte_size
        if self.check_memory_available(pcb):
            self.memory_map.append((pcb.loader, end))
            return True
        return False
    
    def free_memory(self, start, size):
        """ Free memory and update memory map. """
        end = start + size
        if (start, end) in self.memory_map:
            self.memory_map.remove((start, end))
            self.memory[start:end] = [0] * (end - start) # Clear memory
            return True
        return False
    
    from hardware.Memory import Memory
from struct import unpack


class MemoryManager:
    def __init__(self, system, size):
        self.memory = Memory(size)
        self.system = system
        self.memory_map = []

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
            # print("File not found")
            self.system_code(109, f"File not found: {filepath}")
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
    
    def allocate_memory(self, pcb):
        """ Allocate memory if available and update memory map. """
        start = pcb.loader
        end = start + pcb.byte_size
        if self.check_memory_available(pcb):
            self.memory_map.append((start, end))
            return True
        return False
    
    def load_to_memory(self, pcb):
        """ Load program into memory if space is available. """
        if not self.allocate_memory(pcb):
            self.system_code(102, f"Failed to allocate memory for {pcb.file}")
            return None
        

        # Check if another pcb is already loaded at the loader address and not terminated
        # for other_pcb in self.system.ready_queue:
        #     if ((other_pcb != pcb and other_pcb['file'] != pcb['file']) and # Make sure it's not the same program
        #        (other_pcb['state'] not in ['TERMINATED', 'NEW'])): # Make sure it's not terminated or new
        #         if ((pcb['loader'] < other_pcb['code_end'] and pcb['loader'] > other_pcb['code_start']) or 
        #            (pcb['code_end'] > other_pcb['loader'] and pcb['code_end'] < other_pcb['code_end'])):
        #             self.system_code(102, pcb['file'])
        #             return None
    
        try :
            with open(pcb.file, 'rb') as f:
                f.seek(12) # Skip header
                self.memory[pcb.loader : pcb.loader + pcb.byte_size] = f.read(pcb.byte_size)
                self.system.print(f"Loaded {pcb.file} to memory")
                return True
        except Exception as e:
            self.system_code(100, f"Error loading {pcb['file']}: {e}")
            self.free_memory(pcb)
            return None
        
    def free_memory(self, pcb):
        """ Free memory and update memory map. """
        start = pcb.loader
        end = start + pcb.byte_size
        if (start, end) in self.memory_map:
            self.memory_map.remove((start, end))
            self.memory[start:end] = [0] * (end - start) # Clear memory
            return True
        return False
    
    # def release_resources(self, pcb):
    #     loader = pcb['loader']
    #     code_end = pcb['code_end']
    #     self.memory[loader:code_end+1] = [0] * (code_end - loader + 1)
    #     self.system.print(f"Released resources for {pcb}")

    def system_code(self, code, *args):
        self.system.system_code(code, *args)

    def check_memory_available(self, pcb):
        start = pcb.loader
        end = start + pcb.byte_size

        for allocated_start, allocated_end in self.memory_map:
            if not (end <= allocated_start or start >= allocated_end):
                return False 
        return True
            
        # for existing_job in self.system.ready_queue:
        #     if ((pcb['loader'] < existing_job['code_end'] and pcb['loader'] + pcb['byte_size'] > existing_job['code_start']) or 
        #        (pcb['loader'] + pcb['byte_size'] > existing_job['code_start'] and pcb['loader'] < existing_job['code_end'])):
        #         # There is overlap in memory
        #         return False
    
    
        
    
    
    # def release_resources(self, pcb):
    #     loader = pcb['loader']
    #     code_end = pcb['code_end']
    #     self.memory[loader:code_end+1] = [0] * (code_end - loader + 1)
    #     self.system.print(f"Released resources for {pcb}")

    def system_code(self, code, *args):
        self.system.system_code(code, *args)

    # def check_memory_available(self, pcb):
    #     start = pcb.loader
    #     end = start + pcb.byte_size

    #     for allocated_start, allocated_end in self.memory_map:
    #         if not (end <= allocated_start or start >= allocated_end):
    #             return False 
            
    #     # for existing_job in self.system.ready_queue:
    #     #     if ((pcb['loader'] < existing_job['code_end'] and pcb['loader'] + pcb['byte_size'] > existing_job['code_start']) or 
    #     #        (pcb['loader'] + pcb['byte_size'] > existing_job['code_start'] and pcb['loader'] < existing_job['code_end'])):
    #     #         # There is overlap in memory
    #     #         return False
    #     return True