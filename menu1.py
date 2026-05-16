import pygame
import os
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK, RED # Impor dari config.py

# Tambahkan fungsi resource_path di atas
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Fungsi untuk menampilkan menu awal
def main_game_menu(screen):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path(os.path.join("sound", "soundMenu.mp3")))
    pygame.mixer.music.play()  # Looping terus

    font_title = pygame.font.Font(resource_path(os.path.join("font", "youmurdererbb_reg.ttf")), 90)
    font_header = pygame.font.Font(resource_path(os.path.join("font", "youmurdererbb_reg.ttf")), 120)
    font_header2 = pygame.font.Font(resource_path(os.path.join("font", "youmurdererbb_reg.ttf")), 60)
    
    text = font_title.render("start", True, WHITE)
    header_text = font_header.render("Sabrr..", True, WHITE)
    header2_text = font_header2.render("Nanti juga nyerang", True, WHITE)
    header_rect = header_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 185))
    header2_rect = header2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Awal")


    game_state = "Menu"
    blink = False
    blink_count = 0
    blink_timer = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop music sebelum keluar
                running = False
                return "QUIT"  

            if game_state == "Menu":
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                
                if event.type == pygame.MOUSEBUTTONDOWN: #ketika mouse ditekan
                    if text_rect.collidepoint(event.pos):
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()

        if game_state == "Menu":
            screen.fill(BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            show_text = True
            
            if text_rect.collidepoint(mouse_pos):
                text_display = font_title.render("start", True, RED)  # Merah
            else:
                text_display = text  # Putih

            if blink:
                # Setiap 100ms, toggle tampil/hilang,)
                now = pygame.time.get_ticks()
                if (now - blink_timer) > 100:
                    blink_timer = now
                    blink_count += 1
                show_text = blink_count % 2 == 0
                if blink_count >= 2: 
                    pygame.mixer.music.stop()
                    blink = False  # Stop blinkingkedip
                    return "STAGE1" 
                 
            screen.blit(header_text, header_rect)
            screen.blit(header2_text, header2_rect)
            if show_text:
                screen.blit(text_display, text_rect)  
        
        pygame.display.update()

pygame.quit()


