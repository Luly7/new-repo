import random

class Scheduler:
    def __init__(self, system):
        self.system = system

    def schedule_jobs(self):
        self._sort_ready_queue()

        while self.system.job_queue or self.system.ready_queue or self.system.io_queue: # If theres programs one of the queues
            # Move jobs from job queue to ready queue, if current time is past programs arrival time
            self.system.print(f"\n========== Clock: {self.system.clock.time} ==========")
            self.check_new_jobs()
            self.check_io_complete()

            # Run the next job in the ready queue, FCFS
            if self.system.ready_queue:
                pcb = self.schedule_job()
                self.handle_process_state(pcb)
                if self.system.verbose:
                    self.system.display_state_table()
            else:
                # If no job is ready increment clock
                self.system.clock += 1
                self.system.print("No jobs ready to run")

    def check_new_jobs(self):
        """ Move jobs from job queue to ready queue, if current time is past programs arrival time."""
        i = 0
        while i < len(self.system.job_queue): # Iterate through job queue
            pcb = self.system.job_queue[i]
            if self.system.clock.time < pcb.arrival_time: # Once we find a job that has not arrived yet, break out of loop
                break

            # Ensure memory is available without overlapping with other processes
            if self.system.handle_check_memory_available(pcb):
                if self.system.handle_load_to_memory(pcb):
                    self.system.ready_queue.insert(0, self.system.job_queue.pop(i)) # move job from job queue to ready queue
                else:
                    self.system.print(f"Error loading {pcb} to memory")
                    return None
            else:
                i += 1
        

    def schedule_job(self):
        """ Schedule the next job in the ready queue."""
        pcb = self.system.ready_queue.pop()
        pcb.ready(self.system.clock.time) # mark it as ready
        self.system.print(f"\nScheduling {pcb}")
        self.system.run_pcb(pcb)
        return pcb
        
        
    def _sort_ready_queue(self):
        """ Sort the ready queue by arrival time."""
        self.system.ready_queue.sort(key=lambda x: x.arrival_time)

    def handle_process_state(self, pcb):
        """ Handle the state of the process after running."""
        if pcb.state == 'TERMINATED':
            self.system.handle_free_memory(pcb)
            self.system.terminated_queue.append(pcb)
        elif pcb.state == 'WAITING':
            wait_until = self.system.clock.time + random.randint(1, 50)
            pcb.wait_until = wait_until
            self.system.print(f"{pcb} waiting until {wait_until}")
            self.system.io_queue.append(pcb)
        elif pcb.state == 'READY':
            self.system.ready_queue.append(pcb)
        else:
            self.system.print(f"Error: Invalid state {pcb.state} for {pcb}")

    def check_io_complete(self):
        for i, pcb in enumerate(self.system.io_queue):
            if self.system.clock.time >= pcb.wait_until:
                self.system.io_queue.pop(i)
                self.system.ready_queue.append(pcb)
                self.system.print(f"IO complete for {pcb}")
