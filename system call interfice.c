#include <stdint.h>
#include "video.h"
#define SYS_WRITE 1
void syscall_handler() {
    uint32_t syscall_num;
    __asm__ volatile ("movl %%eax, %0" : "=r"(syscall_num));
    switch(syscall_num) {
        case SYS_WRITE: {
            char *str;
            __asm__ volatile ("movl %%ebx, %0" : "=r"(str));
            video_print(str);
            break;
        }
        default:
            break;
    }
}