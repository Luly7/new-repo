
# OS Implementation by Jason Petersen
CS6510 - Spring 2025

# Start
`python main.py`

Start the OS by running the main.py file. This starts the system and the command line interface

# Load a program
`shell > load test.osx [-v]`

By starting the program you should see the prompt `shell >`. Type `load` followed by the program name. Optionally you can type `-v` to laod the program in verbose mode.

# Run a program
`shell > run [-v]`

To run a program simply type run, you will get a confirmation when the program has finished running. Optionally you can type `-v` to run the program in verbose mode. 

# Check memory
`shell > coredump -v`

If you would like to see the contents of the memory type `coredump`. WIthout the optional `-v` flag the contents of memory will be saved to the file `memory.txt`, with the flag the contents of memory will be displayed in the terminal.

# Switch to bash mode
`shell > bash`

To switch the command line interface to the bash version type `bash` into the terminal. The command line will now appear as `bash > `.

At the moment bash mode does not do anything, including loading and running programs. It's simply a placeholder to be implemented later.

# Switch to shell mode
`bash > shell`

To switch back to shell mode type `shell` into the bash command line. In shell mode you can load and run programs.