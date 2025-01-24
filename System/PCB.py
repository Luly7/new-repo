class PCB:
    def __init__(self, pid, pc, registers, state):
        self.pid = pid
        self.pc = pc
        self.registers = registers
        self.state = state

    def __str__(self):
        return f"PID: {self.pid}, PC: {self.pc}, Registers: {self.registers}, State: {self.state}"
    
    def set_state(self, new_state):
        self.state = new_state
    
    def get_state(self):
        return self.state