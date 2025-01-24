import sys
import struct

MEMORY_SIZE = 1024
memory = bytearray(MEMORY_SIZE)


def load_osx(filepath):
    global memory

    # with open(filepath, 'rb') as f:
    #     print(f.read())
    
    # with open(filepath, 'rb') as f:

    #     byte = f.read(1)
    #     while byte:
    #         print(byte, struct.unpack('B', byte))
    #         byte = f.read(1)


    fRun = True
    if fRun:
        with open(filepath, 'rb') as f:

            header = f.read(12)
            byteSize, pc, loader = struct.unpack('III', header)

            print(header)
            print(byteSize, pc, loader)

            chunk = f.read(6)
            while chunk:
                print(chunk)
                argv = struct.unpack('6B', chunk)
                print(argv)
                chunk = f.read(6)
        
        
def main():
    load_osx("test.osx")

if __name__ == "__main__":
    main()
