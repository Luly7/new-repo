from cli.CommandLineInterface import CommandLineInterface
from System import System

if __name__ == '__main__':
    system = System()
    cli = CommandLineInterface(system)
    cli.run()