; bootloader.asm
[BITS 16]
[ORG 0x7C00]           ; آدرس شروع بوت‌لودر در حافظه

start:
    ; تنظیم اولیه رجیسترهای قطعه‌ای (Segment Registers)
    xor ax, ax
    mov ds, ax
    mov es, ax

    ; نمایش پیام بوت
    mov si, msg
    call print_string

    ; انتظار برای فشردن یک کلید
    mov ah, 0
    int 0x16

    ; (در سیستم واقعی باید سکتورهای بعدی کرنل را از دیسک بخوانیم)
    ; فرض می‌کنیم کرنل از قبل در آدرس 0x1000 بارگذاری شده است.
    ; تنظیم DS به آدرس 0x1000
    mov ax, 0x1000
    mov ds, ax

    ; پرش به تابع kernel_main در کرنل
    jmp 0x1000:kernel_main

hang:
    jmp hang

print_string:
    mov ah, 0x0E         ; تابع BIOS برای چاپ کاراکتر به صورت teletype
.print_loop:
    lodsb                ; بارگذاری یک بایت از آدرس DS:SI در AL و افزایش SI
    cmp al, 0
    je .done
    int 0x10             ; فراخوانی BIOS برای چاپ کاراکتر در AL
    jmp .print_loop
.done:
    ret

msg db 'Bootloader Loaded! Press any key to continue...', 0

times 510 - ($ - $$) db 0  ; پر کردن سکتور تا 510 بایت
dw 0xAA55                ; امضای بوت (Boot Signature)