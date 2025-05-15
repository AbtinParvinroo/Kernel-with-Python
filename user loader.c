#include <stdint.h>

#define SECTOR_SIZE       512
#define PROGRAM_SECTOR    10
#define PROGRAM_LOAD_ADDR 0x100000
void read_sector(uint32_t lba, void *buffer) {
}
void load_user_program() {
    read_sector(PROGRAM_SECTOR, (void *)PROGRAM_LOAD_ADDR);
    void (*entry)() = (void (*)())PROGRAM_LOAD_ADDR;
    entry();
}