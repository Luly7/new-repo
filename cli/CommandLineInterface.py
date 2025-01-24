from .Shell import ShellMode
from .Bash import BashMode


class CommandLineInterface:
    def __init__(self, system):
        self.modes = {
            "shell": ShellMode(system),
            "bash": BashMode(system)
        }
        self.current_mode = "shell"

    def run(self):
        while True:
            mode = self.modes[self.current_mode].run()
            if mode is None:
                break
            self.current_mode = mode