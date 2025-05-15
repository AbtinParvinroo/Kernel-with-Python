#include <stdio.h>
#include <stdint.h>
typedef struct context {
    uint32_t eax, ebx, ecx, edx;
    uint32_t esi, edi, ebp, esp;
    uint32_t eip, eflags;
} context_t;
typedef struct task_struct {
    context_t context;
    struct task_struct *next;
} task_t;
task_t *current_task = NULL;
task_t *task_list = NULL;
void save_context(context_t *context) {
    __asm__ volatile (
        "movl %%eax, %0\n"
        "movl %%ebx, %1\n"
        "movl %%ecx, %2\n"
        "movl %%edx, %3\n"
        "movl %%esi, %4\n"
        "movl %%edi, %5\n"
        "movl %%ebp, %6\n"
        "movl %%esp, %7\n"
        "pushfl\n"
        "popl %8\n"
        "call 1f\n"
        "1: popl %9\n"
        : "=m"(context->eax), "=m"(context->ebx), "=m"(context->ecx), "=m"(context->edx),
            "=m"(context->esi), "=m"(context->edi), "=m"(context->ebp), "=m"(context->esp),
            "=m"(context->eflags), "=m"(context->eip)
    );
}
void restore_context(context_t *context) {
    __asm__ volatile (
        "movl %0, %%eax\n"
        "movl %1, %%ebx\n"
        "movl %2, %%ecx\n"
        "movl %3, %%edx\n"
        "movl %4, %%esi\n"
        "movl %5, %%edi\n"
        "movl %6, %%ebp\n"
        "movl %7, %%esp\n"
        "pushl %8\n"
        "popfl\n"
        "jmp *%9\n"
        : : "m"(context->eax), "m"(context->ebx), "m"(context->ecx), "m"(context->edx),
            "m"(context->esi), "m"(context->edi), "m"(context->ebp), "m"(context->esp),
            "m"(context->eflags), "m"(context->eip)
    );
}
void schedule() {
    if (current_task == NULL || current_task->next == NULL)
        return;
    save_context(&current_task->context);
    current_task = current_task->next;
    restore_context(&current_task->context);
}
void timer_interrupt_handler() {
    schedule();
}
void add_task(task_t *task) {
    if (!task) return;
    if (task_list == NULL) {
        task_list = task;
        task->next = task_list;
        current_task = task_list;
    } else {
        task_t *temp = task_list;
        while (temp->next != task_list) {
            temp = temp->next;
        }
        temp->next = task;
        task->next = task_list;
    }
}