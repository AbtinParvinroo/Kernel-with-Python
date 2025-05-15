void kernel_main() {
    char *msg = "hello from kernel! \n";
    char * p = msg;
    while (*p)
    {
        __asm__ volatile (
            "mov ah, 0x0E\n"
            "mov al, %0\n"
            "int 0x10\n"
            : "r"(*p)
        );
        p++;
    }
    while (1);
}