class Memory:
    def __init__(self, size='1K'):
        self.size = self.calculateSize(size)
        self.cols = 6
        self.rows = self.size // self.cols
        # self.memory = [bytearray(self.cols) for _ in range(self.rows)]
        self.memory = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.memory[0][0] = 0 # first byte is reserved for system mode
                                 # 0 = kernal mode
                                 # 1 = user mode

    def calculateSize(self, size):
        sizeInt = int(size[:-1])
        sizeChar = size[-1]

        if sizeChar == 'B':
            return sizeInt
        if sizeChar == 'K':
            return sizeInt * 1024
        if sizeChar == 'M':
            return sizeInt * 1024 * 1024
        if sizeChar == 'G':
            return sizeInt * 1024 * 1024 * 1024
    def __repr__(self):
        return f"<Memory size={self.size} bytes>"

    def __str__(self):
        return f"Memory(size={self.size} bytes)"
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.memory[key]
        elif isinstance(key, slice):
            return self.memory[key]
        else:
            raise TypeError('Tried to get from memory with invalid access type.')
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.memory[key] = value
        elif isinstance(key, slice):
            self.memory[key] = value
        else:
            raise TypeError("Tried to store in memory with invalid access type")

    def __len__(self):
        return len(self.memory)
    
    
        
if __name__ == '__main__':
    memory = Memory('20B')
    print(memory[0][0])
    memory[0][0] = 0x00
    print(memory[0][0])