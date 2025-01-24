class Clock:
    def __init__(self, time: int = 0):
        self.time = time

    def __str__(self):
        return str(self.time)
    
    def __add__(self, other):
        self.time += other
        return self
    
    def increment(self):
        self.time += 1
        return self