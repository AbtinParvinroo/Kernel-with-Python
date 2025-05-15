BITS 16
ORG 0x7C00  ; محل لود شدن بوت‌لودر در RAM

; ---------------------
; مرحله 1: فعال کردن A20 Line
; ---------------------
set_a20:
    in al, 0x92
    or al, 2
    out 0x92, al

; ---------------------
; مرحله 2: ساخت GDT
; ---------------------
lgdt [gdt_descriptor]  ; بارگذاری جدول GDT

; ---------------------
; مرحله 3: سویچ به Protected Mode
; ---------------------
cli                   ; غیرفعال کردن وقفه‌ها
mov eax, cr0
or eax, 1
mov cr0, eax          ; فعال کردن Protected Mode
jmp CODE_SEG:init_pm  ; پرش به کد 32 بیتی

; ---------------------
; جدول GDT
; ---------------------
gdt_start:
    dq 0x0000000000000000  ; Null Segment
    dq 0x00CF9A000000FFFF  ; Code Segment (32-bit)
    dq 0x00CF92000000FFFF  ; Data Segment (32-bit)
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; ---------------------
; کد 32 بیتی کرنل
; ---------------------
BITS 32
init_pm:
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov esp, 0x90000  ; تنظیم استک
    call kernel_main  ; صدا زدن کرنل C

hang:
    hlt
    jmp hang

CODE_SEG equ 0x08
DATA_SEG equ 0x10

times 510-($-$$) db 0
dw 0xAA55   ; امضای بوت سکتور