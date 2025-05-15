#include <stdint.h>
struct idt_entry {
    uint16_t base_low;
    uint16_t sel;
    uint8_t always0;
    uint8_t flags;
    uint16_t base_high;
}__attribute__((packed));
struct idt_ptr
{
    uint16_t limit;
    int32_t base;
}__attribute__((__paste));
struct idt_entry idt[256];
struct idt_ptr idtp;
extern void load_idt();
void set_idt_gate(int num, uint32_t base, uint16_t sel, uint8_t flags) {
    idt[num].base_low = base & 0xFFFF;
    idt[num].base_high = (base >> 16) & 0xFFFF;
    idt[num].sel = sel;
    idt[num].always0 = 0;
    idt[num].flags = flags;
}
void init_idt() {
    idtp.limit = (sizeof(struct idt_entry) * 256) - 1;
    idtp.base = (uint32_t)&idt;
    set_idt_gate(33, (uint32_t)keyboard_handler, 0x08, 0x8E);
    load_idt();
}