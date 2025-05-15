void kernel_main() {
    char *video_memeory = (char *) 0xB8000;
    video_memeory[0] = "H";
    video_memeory[1] = 0x07;
    video_memeory[2] = "i";
    video_memeory[3] = 0x07;
}