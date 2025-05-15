class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.free_list = [(0, total_memory)]
        self.allocated_blocks = {}

    def allocate(self, size):
        for i, (start, block_size) in enumerate(self.free_list):
            if block_size >= size:
                allocated_address = start
                self.allocated_blocks[allocated_address] = size
                if block_size == size:
                    self.free_list.pop(i)
                else:
                    self.free_list[i] = (start + size, block_size - size)
                print(f"[MEMORY] Allocated {size}MB at address {allocated_address}.")
                self.print_status()
                return allocated_address
        print("[MEMORY] Not enough memory!")
        return None

    def free(self, address):
        if address not in self.allocated_blocks:
            print(f"[MEMORY] Address {address} not allocated!")
            return False
        size = self.allocated_blocks.pop(address)
        self.free_list.append((address, size))
        self.free_list = sorted(self.free_list, key=lambda x: x[0])
        self.merge_free_list()
        print(f"[MEMORY] Freed {size}MB from address {address}.")
        self.print_status()
        return True

    def merge_free_list(self):
        merged = []
        for block in self.free_list:
            if not merged:
                merged.append(block)
            else:
                last_start, last_size = merged[-1]
                current_start, current_size = block
                if last_start + last_size == current_start:
                    merged[-1] = (last_start, last_size + current_size)
                else:
                    merged.append(block)
        self.free_list = merged

    def print_status(self):
        used = sum(self.allocated_blocks.values())
        free = self.total_memory - used
        print(f"[MEMORY] Total: {self.total_memory}MB, Used: {used}MB, Free: {free}MB")
        print("[MEMORY] Free blocks:", self.free_list)
        print("-" * 50)

if __name__ == "__main__":
    memory_manager = MemoryManager(100) 

    addr1 = memory_manager.allocate(30)
    addr2 = memory_manager.allocate(50)
    addr3 = memory_manager.allocate(40)

    memory_manager.free(addr2)

    addr4 = memory_manager.allocate(40)