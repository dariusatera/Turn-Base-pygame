import pygame
from config import WIDTH, HEIGHT, BLACK, WHITE, GREEN, GREY, RED, GOLD
from partycode import party, draw_hp_bar
from TomboBattle import battle_tombol  # ambil logika gambarnya saja
from LogikaPertarungan import karakter, Slayer, Mage, Healer, Monster, stages, turn_order, stage_1, stage_2, stage_3

pygame.init()

def inti(screen):
    #=======================Buat Import Suara=============================#
    pygame.mixer.init()
    SOUND_END_EVENT = pygame.USEREVENT + 1 # Event untuk mendeteksi akhir musik

    pygame.mixer.music.load(r"C:\Codingan\projactG\sound\Battle.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(SOUND_END_EVENT) # Set event ketika musik selesai

    loop_sound_path = r"C:\Codingan\projactG\sound\Phalanx_Battle_soundtrack.mp3"
    music_playing = False 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle & Party")

    # --- Siapkan font dan tombol seperti di battle_tombol ---
    font_pukul = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)
    font_skill = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)
    font_ulti = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)

    pukul = font_pukul.render("Pukul", True, (255,255,255))
    skill = font_skill.render("Skill", True, (255,255,255))
    ulti = font_ulti.render("CORE", True, (255,255,255))

    pukul_rect = pukul.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2 + 150))
    skill_rect = skill.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2 + 200))
    ulti_rect = ulti.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 250))

    # --- Siapkan posisi dan radius untuk party ---
    positions = [
        (WIDTH // 10, HEIGHT // 2 + 200),
        (WIDTH // 10 + 90, HEIGHT // 2 + 200),
        (WIDTH // 10 + 180, HEIGHT // 2 + 200)
    ]
    radius = 40
    
    # --- Siapkan posisi dan radius untuk monster ---
    monster_positions = [
        (WIDTH // 2 + 100, HEIGHT // 2 - 50),
        (WIDTH // 2 + 190, HEIGHT // 2 - 50)
    ]
    monster_radius = 50
    
    # Load gambar PNG untuk masing-masing karakter
    character_imgs = [
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\slayer.png").convert_alpha(), (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\healer.png").convert_alpha(), (radius*2, radius*2)
        ),
    ]
    
    # Load gambar PNG untuk monster (pastikan file ada)
    monster_imgs = [
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
    ]
    
    monsters = stages[0]  # Ambil stage pertama dari daftar stages

    blink = False
    blink_count = 0
    blink_timer = 0
    blink_target = None

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SOUND_END_EVENT and not music_playing: # Jika musik selesai dan belum diputar ulang
                pygame.mixer.music.load(loop_sound_path) # Ganti dengan musik loop
                pygame.mixer.music.play(-1)
                music_playing = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pukul_rect.collidepoint(event.pos):
                    print("Pukul button di klik")
                    blink = True
                    blink_count = 0
                    blink_timer = pygame.time.get_ticks()
                    blink_target = "pukul"
                elif skill_rect.collidepoint(event.pos):
                    print("Skill button di klik")
                    blink = True
                    blink_count = 0
                    blink_timer = pygame.time.get_ticks()
                    blink_target = "skill"
                elif ulti_rect.collidepoint(event.pos):
                    print("Ulti button di klik")
                    blink = True
                    blink_count = 0
                    blink_timer = pygame.time.get_ticks()
                    blink_target = "ulti"

        screen.fill(BLACK)

        # --- Gambar party ---
        for idx, character in enumerate(party):
            # Ganti lingkaran dengan gambar PNG sesuai urutan karakter
            img_rect = character_imgs[idx].get_rect(center=positions[idx])
            screen.blit(character_imgs[idx], img_rect)
            bar_x = positions[idx][0] - 40
            bar_y = positions[idx][1] + radius + 20
            draw_hp_bar(screen, character, bar_x, bar_y, 80, 10)
        
        # --- Gambar monster ---
        for idx, monster in enumerate(monsters):
            img_rect = monster_imgs[idx].get_rect(center=monster_positions[idx])
            screen.blit(monster_imgs[idx], img_rect)
            bar_x = monster_positions[idx][0] - 50
            bar_y = monster_positions[idx][1] + monster_radius + 20
            draw_hp_bar(screen, monster, bar_x, bar_y, 80, 10)

        # --- Gambar tombol untuk pukul, skill, dan ulti ---
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

        if pukul_rect.collidepoint(mouse_pos):
            pukul_display = font_pukul.render("Pukul", True, (255,50,50))
        else:
            pukul_display = pukul

        if skill_rect.collidepoint(mouse_pos):
            skill_display = font_skill.render("Skill", True, (255,50,50))
        else:
            skill_display = skill

        if ulti_rect.collidepoint(mouse_pos):
            ulti_display = font_ulti.render("CORE", True, (255,215,0))
        else:
            ulti_display = ulti

        if show_pukul:
            screen.blit(pukul_display, pukul_rect)
        if show_skill:
            screen.blit(skill_display, skill_rect)
        if show_ulti:
            screen.blit(ulti_display, ulti_rect)

        pygame.display.update()

    pygame.quit()