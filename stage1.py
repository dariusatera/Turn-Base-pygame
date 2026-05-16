import pygame
import os
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK  # Impor dari config.py

# Tambahkan fungsi resource_path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def stage1(screen):
    pygame.init()
    #=======================Buat Import Suara=============================#
    pygame.mixer.init()
    start_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "Opening.wav")))
    start_sound.play()
    
    #=======================Buat Variabel untuk Fade In=============================#
    font_title = pygame.font.Font(resource_path(os.path.join("font", "youmurdererbb_reg.ttf")), 100)
    text = font_title.render("STAGE1", True, WHITE) 
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Didefinisikan di awal
    pygame.display.set_caption("Menu Stage 1")

    alpha = 0
    fade_in_speed = 5 # Kecepatan fade in 

    #========================Buat Variabel untuk Blinking=============================#
    blink = False # Kondisi blinking
    blink_count = 0 # Hitung jumlah kedipan
    blink_timer = 0 # Timer untuk blinking

    running = True
    clock = pygame.time.Clock() # 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"  # Kembalikan "QUIT" agar main.py bisa keluar
            if alpha == 255 and event.type == pygame.MOUSEBUTTONDOWN: # Ketika mouse ditekan setelah fade in selesai
                if text_rect.collidepoint(event.pos): # Cek apakah mouse berada di atas teks
                    blink = True
                    blink_count = 0
                    blink_timer = pygame.time.get_ticks()

        screen.fill(BLACK)

        # Fade in logic
        if alpha < 255: # Jika alpha kurang dari 255, lakukan fade in
            alpha += fade_in_speed
            if alpha > 255:
                alpha = 255

        # Blinking logic
        show_text = True
        if blink:
            now = pygame.time.get_ticks()
            if (now - blink_timer) > 100:
                blink_timer = now
                blink_count += 1
            show_text = blink_count % 2 == 0
            if blink_count >= 2:  # 1 kali kedip
                return "BATTLE1"  # Kembali ke main.py setelah kedip

        # Blit teks sesuai kondisi
        if not blink:
            # Saat fade in, tampilkan teks dengan alpha
            text_with_alpha = text.copy()
            text_with_alpha.set_alpha(alpha)
            screen.blit(text_with_alpha, text_rect) # Tampilkan teks dengan alpha yang sesuai
        else:
            # Saat blinking, tampilkan/hidden sesuai show_text
            if show_text and alpha == 255: 
                screen.blit(text, text_rect) # Tampilkan teks jika show_text True

        pygame.display.update()
        clock.tick(60)




