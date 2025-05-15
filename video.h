#ifndef VIDEO_H
#define VIDEO_H
#include <stdint.h>
#define VIDEO_MEMORY  0xB8000
#define SCREEN_WIDTH  80
#define SCREEN_HEIGHT 25
#define WHITE_ON_BLACK 0x0F
void video_clear();
void video_print(const char *message);
void video_put_char(char c, int x, int y, uint8_t attr);
void video_scroll();
#endif