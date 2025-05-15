import time

class Kernel:
    def __init__(self):
        self.process_list = []

    def boot(self):
        print("[Boot] Initializing Kernel... ")
        time.sleep(1)
        print("[Boot] Loading system drivers... ")
        time.sleep(1)
        print("[Boot] Starting user processes... ")
        time.sleep(1)
        print("[Boot] Kernel Successfully loaded! ")
        self.run()

    def run(self):
        while True:
            if not self.process_list:
                print("[KERNEL] No processes running. System idle... ")
                time.sleep(2)
            else:
                for process in self.process_list:
                    process.run()

    def add_process(self, process):
        self.process_list.append(process)
        print(f"[KERNEL] New process added: {process.name}")

myKernel = Kernel()
myKernel.boot()