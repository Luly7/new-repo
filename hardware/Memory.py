class Memory:
    def __init__(self, size='1K'):
        self.size = self.calculate_size(size)
        self.cols = 6
        self.rows = self.size // self.cols
        self._memory = bytearray(self.size)
        self._memory[0] = 0 # first byte is reserved for system mode
        # self.memory = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # self.memory[0][0] = 0 # first byte is reserved for system mode
                                 # 0 = kernal mode
                                 # 1 = user mode

    def calculate_size(self, size):
        size_int = int(size[:-1])
        size_char = size[-1]

        if size_char == 'B':
            return size_int
        if size_char == 'K':
            return size_int * 1024
        if size_char == 'M':
            return size_int * 1024 * 1024
        if size_char == 'G':
            return size_int * 1024 * 1024 * 1024
        
    def __repr__(self):
        return f"<Memory size={self.size} bytes>"

    def __str__(self):
        string = ''
        string += f"0: {self._memory[0]:02X}\n"
        l = 1
        for i in range(1, self.rows):
            string += f"{l}-{l+5}: "
            l += 6
            for j in range(self.cols):
                string += f"{self._memory[i * self.cols + j]:02X} "
            string += '\n'
        return string
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._memory[key]
        elif isinstance(key, slice):
            return self._memory[key]
        else:
            raise TypeError('Tried to get from memory with invalid access type.')
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._memory[key] = value
        elif isinstance(key, slice):
            self._memory[key] = value
        else:
            raise TypeError("Tried to store in memory with invalid access type")

    def __len__(self):
        return len(self._memory)
    
