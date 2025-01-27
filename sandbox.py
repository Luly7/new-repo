from System.System import System

def load_into_system(system, filepath):
    return system.load_file(filepath)

def run_pcb(system, pcb):
    system.run_pcb(pcb)

def main():
    system = System()
    filepath = 'test.osx'
    
    pcb = load_into_system(system, filepath)
    run_pcb(system, pcb)
    print(system._CPU.registers)
    
if __name__ == "__main__":
    main()