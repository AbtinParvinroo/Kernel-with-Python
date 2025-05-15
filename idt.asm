BITS 32

global load_idt

load_idt:
    lidt [idt_descriptor] ; بارگذاری IDT در CPU
    sti                   ; فعال کردن وقفه‌ها
    ret

section .data
idt_descriptor:
    dw 256*8-1  ; اندازه IDT (256 ورودی، هر کدام 8 بایت)
    dd idt_start

section .bss
idt_start resb 256*8