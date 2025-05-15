#include <stdint.h>
#define SYS_WRITE 1
static inline void sys_call(uint32_t num, uint32_t arg) {
    __asm__ volatile (
        "int $0x80"
        : 
        : "a"(num), "b"(arg)
    );
}
int main() {
    sys_call(SYS_WRITE, (uint32_t)"Hello from user space!\n");
    while (1);
    return 0;
}