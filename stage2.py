import pygame
import os
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK  # Impor dari config.py

# Tambahkan fungsi resource_path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def stage2(screen):
    pygame.init()
    pygame.mixer.init()
    start_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "Opening.wav")))
    start_sound.play()

    font_title = pygame.font.Font(resource_path(os.path.join("font", "youmurdererbb_reg.ttf")), 100)
    text = font_title.render("STAGE2", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.display.set_caption("Menu Stage 2")

    alpha = 0
    fade_in_speed = 5

    blink = False
    blink_count = 0
    blink_timer = 0

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if alpha >= 255 and event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    blink = True
                    blink_count = 0
                    blink_timer = pygame.time.get_ticks()

        screen.fill(BLACK)

        # Fade in logic
        if alpha < 255:
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
            if blink_count >= 2:
                return "BATTLE2"

        # Blit teks sesuai kondisi
        if not blink:
            text_with_alpha = text.copy()
            text_with_alpha.set_alpha(alpha)
            screen.blit(text_with_alpha, text_rect)
        else:
            if show_text and alpha == 255:
                screen.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)




