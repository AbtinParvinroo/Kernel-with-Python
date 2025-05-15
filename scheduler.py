from queue import Queue
import threading
import time

class Process:
    def __init__(self, name, execution_time, time_slice):
        self.name = name
        self.execution_time = execution_time
        self.time_slice = time_slice
        self.remaining_time = execution_time

    def run(self):
        while True:
            print(f"[PROCESS] {self.name} is running for {self.time_slice} seconds... ")
            time.sleep(self.time_slice)
            self.remaining_time -= self.time_slice
            if self.remaining_time > 0:
                print(f"[PROCESS] {self.name} has finished execution. ")
            else:
                print(f"[PROCESS] {self.name} has finished execution.")

class Scheduler:
    def __init__(self):
        self.process_queue = Queue()

    def add_process(self, process):
        self.process_queue.append(process)
        print(f"[SCHEDULER] Added process: {process.name}")

    def run(self):
        active_threads = []
        while not self.process_queue.empty():
            process = self.process_queue.get()
            process.start()
            active_threads.append(process)
        for process in active_threads:
            process.join()
        print("[SCHEDULER] All processes finished.")

scheduler = Scheduler()
scheduler.add_process(Process("Process 1", execution_time=5, time_slice=1))
scheduler.add_process(Process("Process 2", execution_time=7, time_slice=1))
scheduler.add_process(Process("Process 3", execution_time=3, time_slice=1))

print("[KERNEL] Starting Scheduler with Round Robin Scheduling...")
scheduler.run()