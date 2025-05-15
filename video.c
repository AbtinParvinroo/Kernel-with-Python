#include "video.h"
static uint16_t *video_memory = (uint16_t *) VIDEO_MEMORY;
static uint8_t cursor_x = 0, cursor_y = 0;
void video_clear() {
    for (int y = 0; y < SCREEN_HEIGHT; y++) {
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            video_put_char(' ', x, y, WHITE_ON_BLACK);
        }
    }
    cursor_x = 0;
    cursor_y = 0;
}
void video_put_char(char c, int x, int y, uint8_t attr) {
    int index = y * SCREEN_WIDTH + x;
    video_memory[index] = (attr << 8) | c;
}
void video_scroll() {
    if (cursor_y >= SCREEN_HEIGHT) {
        for (int y = 1; y < SCREEN_HEIGHT; y++) {
            for (int x = 0; x < SCREEN_WIDTH; x++) {
                video_memory[(y - 1) * SCREEN_WIDTH + x] = video_memory[y * SCREEN_WIDTH + x];
            }
        }
        for (int x = 0; x < SCREEN_WIDTH; x++) {
            video_put_char(' ', x, SCREEN_HEIGHT - 1, WHITE_ON_BLACK);
        }
        cursor_y = SCREEN_HEIGHT - 1;
    }
}
void video_print(const char *message) {
    while (*message) {
        if (*message == '\n') {
            cursor_x = 0;
            cursor_y++;
        } else {
            video_put_char(*message, cursor_x, cursor_y, WHITE_ON_BLACK);
            cursor_x++;
            if (cursor_x >= SCREEN_WIDTH) {
                cursor_x = 0;
                cursor_y++;
            }
        }
        message++;
    }
    video_scroll();
}