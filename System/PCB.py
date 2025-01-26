class PCB:
    def __init__(self, pid, pc, registers, state):
        self.pid = pid
        self.pc = pc
        self.registers = registers
        self.state = state
        self.states = ['NEW', 'READY', 'RUNNING', 'WAITING', 'TERMINATED']
        self.start_line = None
        self.end_line = None
        self.execution_time = None
        self.arrival_time = None
        self.start_time = None
        self.end_time = None
        self.file = None

    def __str__(self):
        return f"PCB(pid={self.pid}, file={self.file}, state={self.state})"
        
    def __repr__(self):
        return f"PID: {self.pid}, PC: {self.pc}, Registers: {self.registers}, State: {self.state}"
        
    def __getitem__(self, key):
        return getattr(self, key)
    
    def set_state(self, new_state):
        self.state = new_state
    
    def get_state(self):
        return self.state
    
    def get_pid(self):
        return self.pid
    
    def get_execution_time(self):
        return self.execution_time
    
    def set_execution_time(self, time):
        self.execution_time = time

    def set_start_line(self, line):
        self.start_line = line 

    def set_end_line(self, line):
        self.end_line = line

    def get_arrival_time(self):
        return self.arrival_time
    
    def set_arrival_time(self, time):    
        self.arrival_time = time

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time

    def set_file(self, file):
        self.file = file