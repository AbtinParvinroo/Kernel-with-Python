from queue import PriorityQueue
import threading
import time

class InterruptHandler:
    def __init__(self):
        self.interrupts = {}
        self.interrupt_queue = PriorityQueue()
        self.running = True
        self.thread = threading.Thread(target=self._process_interrupts)
        self.thread.daemon = True
        self.thread.start()

    def register_interrupt(self, interrupt_code, handler, priority=10):
        self.interrupts[interrupt_code] = (priority, handler)
        print(f"[INTERRUPT] Registered interrupt {interrupt_code} with priority {priority}.")

    def unregister_interrupt(self, interrupt_code):
        if interrupt_code in self.interrupts:
            del self.interrupts[interrupt_code]
            print(f"[INTERRUPT] Unregistered interrupt {interrupt_code}.")
        else:
            print(f"[INTERRUPT] Interrupt {interrupt_code} not registered.")

    def trigger_interrupt(self, interrupt_code):
        if interrupt_code in self.interrupts:
            priority, _ = self.interrupts[interrupt_code]
            self.interrupt_queue.put((priority, interrupt_code))
            print(f"[INTERRUPT] Interrupt {interrupt_code} triggered.")
        else:
            print(f"[INTERRUPT] Unknown interrupt: {interrupt_code}.")

    def _process_interrupts(self):
        while self.running:
            if not self.interrupt_queue.empty():
                priority, code = self.interrupt_queue.get()
                if code in self.interrupts:
                    _, handler = self.interrupts[code]
                    print(f"[INTERRUPT] Handling interrupt {code} with priority {priority}.")
                    handler()
                self.interrupt_queue.task_done()
            else:
                time.sleep(0.1)

    def stop(self):
        self.running = False
        self.thread.join()

def keyboard_interrupt():
    print("[HANDLER] Keyboard interrupt handled.")

def timer_interrupt():
    print("[HANDLER] Timer interrupt handled.")

if __name__ == "__main__":

    ih = InterruptHandler()

    ih.register_interrupt(0x01, keyboard_interrupt, priority=5)
    ih.register_interrupt(0x02, timer_interrupt, priority=10)
    
    ih.trigger_interrupt(0x02)
    time.sleep(0.2)
    ih.trigger_interrupt(0x01)
    time.sleep(0.2)
    ih.trigger_interrupt(0xFF)
    
    time.sleep(1)
    
    ih.stop()