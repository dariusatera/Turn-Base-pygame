import pygame
import os
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK, RED, GOLD  # Impor dari config.py

# Tambahkan fungsi resource_path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def battle_tombol(screen):
    pygame.init()
    font_path = resource_path(os.path.join("font", "youmurdererbb_reg.ttf"))
    font_pukul = pygame.font.Font(font_path, 60)
    font_skill = pygame.font.Font(font_path, 60)
    font_ulti = pygame.font.Font(font_path, 60)
    
    pukul = font_pukul.render("Pukul", True, WHITE)
    skill = font_skill.render("Skill", True, WHITE)
    ulti = font_ulti.render("CORE", True, WHITE)
        
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Awal")

    game_state = "Menu"
    blink = False
    blink_count = 0
    blink_timer = 0
    blink_target = None  # Untuk tahu tombol mana yang sedang kedip

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "QUIT"  

            if game_state == "Menu":
                #Mencitakan posisi tombol (untuk di klik)
                pukul_rect = pukul.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2 + 150))
                skill_rect = skill.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2 + 200))
                ulti_rect = ulti.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 250))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pukul_rect.collidepoint(event.pos):
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "pukul"
                    elif skill_rect.collidepoint(event.pos):
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "skill"
                    elif ulti_rect.collidepoint(event.pos):
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "ulti"

        if game_state == "Menu":
            screen.fill(BLACK)
            pukul_rect = pukul.get_rect(center=(WIDTH // 2 + 300 , HEIGHT // 2 + 150))
            skill_rect = skill.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2 + 200))
            ulti_rect = ulti.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 250))

            # Hover effect
            if pukul_rect.collidepoint(mouse_pos):
                pukul_display = font_pukul.render("Pukul", True, RED)
            else:
                pukul_display = pukul

            if skill_rect.collidepoint(mouse_pos):
                skill_display = font_skill.render("Skill", True, RED)
            else:
                skill_display = skill

            if ulti_rect.collidepoint(mouse_pos):
                ulti_display = font_ulti.render("CORE", True, GOLD)
            else:
                ulti_display = ulti

            # Blinking logic
            show_pukul = True
            show_skill = True
            show_ulti = True
            if blink:
                now = pygame.time.get_ticks()
                if (now - blink_timer) > 100:
                    blink_timer = now
                    blink_count += 1
                if blink_target == "pukul":
                    show_pukul = blink_count % 2 == 0
                elif blink_target == "skill":
                    show_skill = blink_count % 2 == 0
                elif blink_target == "ulti":
                    show_ulti = blink_count % 2 == 0
                if blink_count >= 2:
                    blink = False
                    if blink_target == "pukul":
                        return "PUKUL"
                    elif blink_target == "skill":
                        return "SKILL"
                    elif blink_target == "ulti":
                        return "ULTI"

            # Tampilkan tombol
            if show_skill:
                screen.blit(skill_display, skill_rect)
            if show_ulti:
                screen.blit(ulti_display, ulti_rect)
            if show_pukul:
                screen.blit(pukul_display, pukul_rect)

            pygame.display.update()