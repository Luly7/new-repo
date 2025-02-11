class Scheduler:
    def __init__(self, system):
        self.system = system

    def schedule_jobs(self):
        self.system.job_queue.sort(key=lambda x: x.arrival_time) # sort based on arrival time

        while self.system.job_queue or self.system.ready_queue: # If theres programs in the job queue or ready queue
            # Move jobs from job queue to ready queue, if current time is past programs arrival time
            while self.system.job_queue and self.system.clock.time >= self.system.job_queue[0].arrival_time:
                job = self.system.job_queue.pop(0) # Get the job
                self.system.ready_queue.append(job) # add it to the ready queue
                job.ready() # mark it as ready
                self.system.print('')
                self.system.print(f"Scheduling job: {job}")

            # Run the next job in the ready queue, FCFS
            if self.system.ready_queue:
                job = self.system.ready_queue.pop(0) # Get the first job in the ready queue
                job['start_time'] = self.system.clock.time # Mark the start time
                job['waiting_time'] = job['start_time'] - job['arrival_time'] # Mark the waiting time
                loaded = self.system.memoryManager._load_to_memory(job) # Load the program to memory
                if loaded:
                    self.system.run_pcb(job) # Run the program
            else:
                # If no job is ready increment clock
                self.system.clock += 1