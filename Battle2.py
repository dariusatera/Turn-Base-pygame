import pygame
import random
import os
import sys
from config import WIDTH, HEIGHT, BLACK, WHITE, GREEN, GREY, RED, GOLD
from partycode import party, draw_hp_bar
from TomboBattle import battle_tombol  # ambil logika gambarnya saja
from LogikaPertarungan import (
    karakter, Slayer, Mage, Healer, Monster, stages, turn_order, stage_1, stage_2, stage_3
)

# Tambahkan fungsi resource_path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()

def Battle2(screen):
    # ======================= Buat Import Suara ============================= #
    pygame.mixer.init()
    SOUND_END_EVENT = pygame.USEREVENT + 1  # Event untuk mendeteksi akhir musik

    pygame.mixer.music.load(resource_path(os.path.join("sound", "Phalanx_Battle_soundtrack.mp3")))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_endevent(SOUND_END_EVENT)  # Set event ketika musik selesai

    music_playing = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle & Party2")

    # Load dan scale background
    background_img = pygame.image.load(resource_path(os.path.join("Asset", "ChatGPT Image 28 Mei 2025, 01.03.42.png"))).convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # --- Siapkan font dan tombol --- 
    font_pukul = pygame.font.Font(resource_path(os.path.join("font", "Exquisite Corpse.ttf")), 55)
    font_skill = pygame.font.Font(resource_path(os.path.join("font", "Exquisite Corpse.ttf")), 55)
    font_ulti = pygame.font.Font(resource_path(os.path.join("font", "Exquisite Corpse.ttf")), 55)

    pukul = font_pukul.render("Pukul", True, (255,255,255))
    skill = font_skill.render("Skill", True, (255,255,255))
    ulti = font_ulti.render("CORE", True, (255,255,255))

    pukul_rect = pukul.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2 + 150))
    skill_rect = skill.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2 + 200))
    ulti_rect = ulti.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 250))

    # --- Posisi dan tampilan Party ---
    positions = [
        (WIDTH // 10, HEIGHT // 2 + 200),
        (WIDTH // 10 + 90, HEIGHT // 2 + 200),
        (WIDTH // 10 + 180, HEIGHT // 2 + 200)
    ]
    radius = 40

    # --- Posisi Monster ---
    monster_positions = [
        (WIDTH // 2 + 100, HEIGHT // 2 - 50),
        (WIDTH // 2 + 190, HEIGHT // 2 - 50)
    ]
    monster_radius = 50

    # Load sprite frames untuk karakter
    slayer_frames = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "knight", "slayerF1.png"))).convert_alpha(), (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "knight", "slayerF2.png"))).convert_alpha(), (radius*2, radius*2)
        ),
    ]
    mage_frames = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "mage", "mageF1.png"))).convert_alpha(), (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "mage", "mageF2.png"))).convert_alpha(), (radius*2, radius*2)
        ),
    ]
    healer_frames = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "healer", "healerF1.png"))).convert_alpha(), (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "healer", "healerF2.png"))).convert_alpha(), (radius*2, radius*2)
        ),
    ]

    # Untuk animasi, gunakan frame pertama sebagai default
    character_imgs = [
        slayer_frames[0],
        mage_frames[0],
        healer_frames[0],
    ]

    # Load gambar untuk monster (menggunakan gambar mage sebagai placeholder)
    monster1_frames = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slime", "slime1.png"))).convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slime", "slime2.png"))).convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
    ]
    monster2_frames = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slime", "slime1.png"))).convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slime", "slime2.png"))).convert_alpha(), (monster_radius*2, monster_radius*2)
        ),
    ]
    
    # ==========Slash effect============== #
    slash_img = [ 
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slash", "slash1.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slash", "slash2.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slash", "slash3.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "slash", "slash4.png"))).convert_alpha(), (120, 120)
        )
    ]

    boom_img = [
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom1.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom2.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom3.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom4.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom5.png"))).convert_alpha(), (120, 120)
        ),
        pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("Asset", "boom", "boom6.png"))).convert_alpha(), (120, 120)
        )
    ]

    # Ambil stage pertama dari daftar stages
    monsters = stages[1]

    blink = False
    blink_count = 0
    blink_timer = 0
    blink_target = None

    # ----------------- Variabel Turn-Based ----------------- #
    current_turn_index = 0       # Indeks giliran aktif
    monster_action_started = False
    monster_action_delay = 1000  # Delay aksi monster (ms)
    monster_action_timer = 0

    # Variabel untuk mode aksi player ("pukul", "skill", "ulti")
    player_action_mode = None

    # Helper: mengambil target hidup dari daftar target
    def get_target(target_list):
        for t in target_list:
            if t.is_alive():
                return t
        return None

    # Helper: mendapatkan giliran (hanya karakter hidup)
    def get_turns():
        living_party = [p for p in party if p.is_alive()]
        living_monsters = [m for m in monsters if m.is_alive()]
        return turn_order(living_party, living_monsters)
    
    slayer_frame_idx = 0
    mage_frame_idx = 0
    healer_frame_idx = 0
    
    slayer_frame_timer = pygame.time.get_ticks()
    mage_frame_timer = pygame.time.get_ticks()
    healer_frame_timer = pygame.time.get_ticks()
    
    slayer_frame_interval = 150  # ms antar frame
    mage_frame_interval = 150
    healer_frame_interval = 150

    slash_frame_idx = 0
    slash_frame_timer = pygame.time.get_ticks()
    slash_frame_interval = 50  # ms antar frame slash

    boom_frame_idx = 0
    boom_frame_timer = pygame.time.get_ticks()
    boom_frame_interval = 50  # ms antar frame boom
    
    monster_frames = [monster1_frames, monster2_frames]
    monster_frame_idx = [0, 0]
    monster_frame_timer = [pygame.time.get_ticks(), pygame.time.get_ticks()]
    monster_frame_interval = 150  # ms antar frame
    
    # ----------------- Efek Slash ----------------- # 
    slash_effect = {
        "active": False,
        "target_idx": None,
        "timer": 0,
        "duration": 250  # ms, lama efek slash muncul
    }
    
    boom_scale = 1.4
    boom_effects = []  # List of dict: {"active", "target_idx", "timer", "frame_idx"}
    boom_frame_idx = 0
    boom_frame_timer = pygame.time.get_ticks()
    boom_frame_interval = 50  # ms antar frame boom
    
    
    clock = pygame.time.Clock()
    running = True
    energy = 0  # Tambahkan variabel energi party
    boom_scale = 1.4
    boom_effects = []
    mage_ulti_pending = False
    mage_ulti_sound_played = False
    mage_ulti_actor = None  # Tambahkan ini

    while running:
        clock.tick(30)
        mouse_pos = pygame.mouse.get_pos()

        turns = get_turns()
        if not any(isinstance(c, Monster) for c in turns):
            print("Party menang!")
            return "WIN"
        if not any((not isinstance(c, Monster)) for c in turns):
            print("Monster menang!")
            return "GAMEOVER"
        if not turns:
            return "GAMEOVER"
        if current_turn_index >= len(turns):
            current_turn_index = 0
        current_turn = turns[current_turn_index]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SOUND_END_EVENT and not music_playing:
                pygame.mixer.music.load(resource_path(os.path.join("sound", "Phalanx_Battle_soundtrack.mp3")))
                pygame.mixer.music.play(-1)
                music_playing = True

            # Kontrol player jika giliran anggota party
            if not isinstance(current_turn, Monster):
                if player_action_mode is None and event.type == pygame.MOUSEBUTTONDOWN:
                    # Klik tombol aksi: Basic Attack, Skill, atau Ultimate
                    if pukul_rect.collidepoint(event.pos):
                        print(f"{current_turn.nama} mempersiapkan Basic Attack!")
                        player_action_mode = "pukul"
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "pukul"
                    elif skill_rect.collidepoint(event.pos):
                        if energy >= 1:
                            print(f"{current_turn.nama} mempersiapkan Skill!")
                            player_action_mode = "skill"
                            blink = True
                            blink_count = 0
                            blink_timer = pygame.time.get_ticks()
                            blink_target = "skill"
                        else:
                            print("Energi tidak cukup untuk Skill!")
                    elif ulti_rect.collidepoint(event.pos):
                        if energy >= 2:
                            print(f"{current_turn.nama} mempersiapkan Ultimate!")
                            player_action_mode = "ulti"
                            blink = True
                            blink_count = 0
                            blink_timer = pygame.time.get_ticks()
                            blink_target = "ulti"
                        else:
                            print("Energi tidak cukup untuk Core!")
                elif player_action_mode is not None and event.type == pygame.MOUSEBUTTONDOWN: # aksi player sudah dipilih
                    # Healer - Core (ulti) langsung ke party, tidak pilih target
                    if isinstance(current_turn, Healer) and player_action_mode == "ulti":
                        healer_ulti_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "healersound", "heal.wav")))
                        healer_ulti_sound.play()
                        print(f"{current_turn.nama} menggunakan Ultimate (Core) ke seluruh party!")
                        energy -= 2
                        current_turn.Ultimate(party)
                        player_action_mode = None
                        current_turn_index += 1
                    # Healer - Skill (heal) pilih anggota party
                    elif isinstance(current_turn, Healer) and player_action_mode == "skill":
                        healer_skill_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "healersound", "heal.wav")))
                        healer_skill_sound.play()
                        target_chosen = None
                        for idx, member in enumerate(party):
                            if not member.is_alive():
                                continue
                            party_rect = character_imgs[idx].get_rect(center=positions[idx])
                            if party_rect.collidepoint(event.pos):
                                target_chosen = member
                                break
                        if target_chosen:
                            print(f"{current_turn.nama} menyembuhkan {target_chosen.nama}!")
                            energy -= 1
                            current_turn.Skill(target_chosen)
                            player_action_mode = None
                            current_turn_index += 1
                    else:
                        # Untuk karakter non-Healer atau Healer yang menggunakan Basic Attack/Skill/Ulti ke musuh
                        target_chosen = None
                        chosen_index = None
                        for idx, monster in enumerate(monsters):
                            if not monster.is_alive():
                                continue
                            monster_rect = monster_frames[idx][monster_frame_idx[idx]].get_rect(center=monster_positions[idx])
                            if monster_rect.collidepoint(event.pos):
                                target_chosen = monster
                                chosen_index = idx
                                break
                        if target_chosen:
                            if player_action_mode == "pukul":
                                print(f"{current_turn.nama} melakukan Basic Attack pada {target_chosen.nama}!")
                                current_turn.BasicAttack(target_chosen)
                                energy = min(energy + 1, 4)
                                if isinstance(current_turn, Slayer):
                                    slayer_atk_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "slayersound", "slashpukul.wav")))
                                    slayer_atk_sound.play()
                                    slash_effect["active"] = True
                                    slash_effect["target_idx"] = chosen_index
                                    slash_effect["timer"] = pygame.time.get_ticks()
                                    slash_frame_idx = 0
                                    slash_frame_timer = pygame.time.get_ticks()
                            elif player_action_mode == "skill":
                                energy -= 1
                                if isinstance(current_turn, Mage):
                                    print(f"{current_turn.nama} menggunakan Skill pada {target_chosen.nama}!")
                                    current_turn.Skill(chosen_index, monsters)
                                    boom_scale = 1.4
                                    mage_skill_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "magesound", "explosion-312361 (mp3cut.net).wav")))
                                    mage_skill_sound.play()
                                    boom_effects = [{
                                        "active": True,
                                        "target_idx": chosen_index,
                                        "timer": pygame.time.get_ticks(),
                                        "frame_idx": 0

                                    }]
                                    boom_frame_timer = pygame.time.get_ticks()
                                else:
                                    print(f"{current_turn.nama} menggunakan Skill pada {target_chosen.nama}!")
                                    current_turn.Skill(target_chosen)
                                    if isinstance(current_turn, Slayer):
                                        slayer_skill_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "slayersound", "skillslash.mp3")))
                                        slayer_skill_sound.play()
                                        slash_effect["active"] = True
                                        slash_effect["target_idx"] = chosen_index
                                        slash_effect["timer"] = pygame.time.get_ticks()
                            elif player_action_mode == "ulti":
                                energy -= 2
                                print(f"{current_turn.nama} menggunakan Ultimate pada semua monster!")
                                if isinstance(current_turn, Mage):
                                    boom_scale = 2.0
                                    mage_ulti_pending = True
                                    mage_ulti_sound_played = False
                                    mage_ulti_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "magesound", "audio [vocals] (mp3cut.net).wav")))
                                    mage_ulti_sound.play()
                                    mage_ulti_actor = current_turn  # Actor Mage yang akan melakukan ulti
                                    player_action_mode = None
                                else:
                                    # Tambahkan sound effect untuk Ultimate Slayer
                                    if isinstance(current_turn, Slayer):
                                        slayer_ulti_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "slayersound", "skillslash.mp3")))
                                        slayer_ulti_sound.play()
                                        slash_effect["active"] = True
                                        slash_effect["target_idx"] = chosen_index
                                        slash_effect["timer"] = pygame.time.get_ticks()
                                        slash_frame_idx = 0
                                        slash_frame_timer = pygame.time.get_ticks()
                                    current_turn.Ultimate(target_chosen)
                                    player_action_mode = None
                                    current_turn_index += 1
                            player_action_mode = None
                            current_turn_index += 1  

        # ------------------ Mage ulti: tunggu sound selesai, lalu mainkan boom ------------------ #
        if mage_ulti_pending:
            if not mage_ulti_sound_played and not pygame.mixer.get_busy():
                boom_sound = pygame.mixer.Sound(resource_path(os.path.join("sound", "magesound", "explosion-312361 (mp3cut.net).wav")))
                boom_sound.play()
                if mage_ulti_actor:
                    mage_ulti_actor.Ultimate(monsters)
                boom_effects = []
                for idx, monster in enumerate(monsters):
                    if monster.is_alive():
                        boom_effects.append({
                            "active": True,
                            "target_idx": idx,
                            "timer": pygame.time.get_ticks(),
                            "frame_idx": 0
                        })
                boom_frame_timer = pygame.time.get_ticks()
                mage_ulti_sound_played = True
            if mage_ulti_sound_played and not any(e["active"] for e in boom_effects):
                mage_ulti_pending = False
                mage_ulti_actor = None
                

        # ------------------ Monster Aksi (Random) ------------------ #
        if isinstance(current_turn, Monster):
            if not monster_action_started:
                monster_action_started = True
                monster_action_timer = pygame.time.get_ticks()
            else:  # Jika aksi monster sudah dimulai, cek apakah waktunya untuk melakukan aksi
                if pygame.time.get_ticks() - monster_action_timer > monster_action_delay:
                    action_choice = random.choice(["basic", "skill"])
                    if action_choice == "basic":
                        print(f"{current_turn.nama} (Monster) melakukan Basic Attack!")
                        target = random.choice([hero for hero in party if hero.is_alive()]) 
                        if target:
                            current_turn.BasicAttack(target)
                        else:
                            print("Tidak ada anggota party yang hidup!")
                    else:
                        print(f"{current_turn.nama} (Monster) menggunakan Skill!")
                        target = get_target(party)
                        if target:
                            current_turn.Skill(target)
                        else:
                            print("Tidak ada anggota party yang hidup!")
                    monster_action_started = False
                    current_turn_index += 1
                    
        # ------------------ Animasi ------------------ #
        now = pygame.time.get_ticks()
        # Slayer
        if now - slayer_frame_timer > slayer_frame_interval:
            slayer_frame_idx = (slayer_frame_idx + 1) % len(slayer_frames)
            slayer_frame_timer = now
            character_imgs[0] = slayer_frames[slayer_frame_idx]
        # Mage
        if now - mage_frame_timer > mage_frame_interval:
            mage_frame_idx = (mage_frame_idx + 1) % len(mage_frames)
            mage_frame_timer = now
            character_imgs[1] = mage_frames[mage_frame_idx]
        # Healer
        if now - healer_frame_timer > healer_frame_interval:
            healer_frame_idx = (healer_frame_idx + 1) % len(healer_frames)
            healer_frame_timer = now
            character_imgs[2] = healer_frames[healer_frame_idx]
        # Slash effect animation
        if slash_effect["active"]:
            now = pygame.time.get_ticks()
            if now - slash_frame_timer > slash_frame_interval:
                slash_frame_idx = (slash_frame_idx + 1) % len(slash_img)
                slash_frame_timer = now
        # Boom effect animation
        if boom_effects:
            now = pygame.time.get_ticks()
            if now - boom_frame_timer > boom_frame_interval:
                boom_frame_idx = (boom_frame_idx + 1) % len(boom_img)
                boom_frame_timer = now

        # Update animasi monster
        for i in range(len(monster_frames)):
            if now - monster_frame_timer[i] > monster_frame_interval:
                monster_frame_idx[i] = (monster_frame_idx[i] + 1) % len(monster_frames[i])
                monster_frame_timer[i] = now

        # ------------------ Drawing ------------------ #
        screen.blit(background_img, (0, 0))

        # Gambar party beserta HP bar
        for idx, character in enumerate(party):
            # Jika giliran karakter ini, perbesar sedikit
            if character is current_turn:
                scale_factor = 1.4  # 40% lebih besar
                img = pygame.transform.scale(
                    character_imgs[idx],
                    (
                        int(character_imgs[idx].get_width() * scale_factor),
                        int(character_imgs[idx].get_height() * scale_factor)
                    )
                )
                img_rect = img.get_rect(center=positions[idx])
                screen.blit(img, img_rect)
            else:
                img_rect = character_imgs[idx].get_rect(center=positions[idx])
                screen.blit(character_imgs[idx], img_rect)
            bar_x = positions[idx][0] - 40
            bar_y = positions[idx][1] + radius + 20
            draw_hp_bar(screen, character, bar_x, bar_y, 80, 10)

        # Gambar monster beserta HP bar
        for idx, monster in enumerate(monsters):
            img = monster_frames[idx][monster_frame_idx[idx]]
            if monster is current_turn:
                scale_factor = 1.4  # 40% lebih besar saat giliran monster
                img = pygame.transform.scale(
                    img,
                    (
                        int(img.get_width() * scale_factor),
                        int(img.get_height() * scale_factor)
                    )
                )
            img_rect = img.get_rect(center=monster_positions[idx])
            screen.blit(img, img_rect)

            # Bar HP tepat di bawah gambar monster (center)
            bar_width = 80
            bar_height = 10
            bar_x = img_rect.centerx - bar_width // 2
            bar_y = img_rect.bottom + 5
            draw_hp_bar(screen, monster, bar_x, bar_y, bar_width, bar_height)

        # Efek blink pada tombol
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

        # Gambar tombol aksi
        if pukul_rect.collidepoint(mouse_pos):
            pukul_display = font_pukul.render("Pukul", True, RED)
        else:
            pukul_display = pukul

        if skill_rect.collidepoint(mouse_pos):
            skill_display = font_skill.render("Skill", True, RED)
        elif energy >= 1:
            skill_display = font_skill.render("Skill", True, (139, 0, 0))  # Merah tua
        else:
            skill_display = skill

        if ulti_rect.collidepoint(mouse_pos):
            ulti_display = font_ulti.render("CORE", True, GOLD)
        elif energy >= 2:
            ulti_display = font_ulti.render("CORE", True, (139, 0, 0))
        else:
            ulti_display = ulti

        if show_pukul:
            screen.blit(pukul_display, pukul_rect)
        if show_skill:
            screen.blit(skill_display, skill_rect)
        if show_ulti:
            screen.blit(ulti_display, ulti_rect)

        # Tampilkan energi party
        font_energy = pygame.font.Font(None, 40)
        energy_text = font_energy.render(f"ENERGI: {energy}", True, GOLD)
        screen.blit(energy_text, (WIDTH // 2 - 60, 30))

        font_turn = pygame.font.Font(None, 36)
        turn_text = font_turn.render(f"Giliran: {current_turn.nama}", True, WHITE)
        screen.blit(turn_text, (20, 20))
        
        if player_action_mode is not None:
            font_target = pygame.font.Font(None, 30)
            if isinstance(current_turn, Healer) and player_action_mode == "skill":
                target_text = font_target.render("Pilih anggota party", True, RED)
            else:
                target_text = font_target.render("Pilih target musuh", True, RED)
            screen.blit(target_text, (WIDTH // 2 - 70, HEIGHT - 50)) # Tampilkan pesan di bawah tombol aksi
        
        # Tampilkan efek slash jika aktif
        if slash_effect["active"]:
            idx = slash_effect["target_idx"]
            if idx is not None and idx < len(monster_positions):
                # Gambar efek slash pada monster yang diserang
                rect = slash_img[slash_frame_idx].get_rect(center=monster_positions[idx])
                screen.blit(slash_img[slash_frame_idx], rect)
            # Cek durasi efek
            if pygame.time.get_ticks() - slash_effect["timer"] > slash_effect["duration"]:
                slash_effect["active"] = False
                slash_effect["target_idx"] = None

        # Tampilkan efek boom jika aktif
        if boom_effects:
            for effect in boom_effects:
                if effect["active"]:
                    idx = effect["target_idx"]
                    if idx is not None and idx < len(monster_positions):
                        boom_img_scaled = pygame.transform.scale(
                            boom_img[boom_frame_idx],
                            (
                                int(boom_img[boom_frame_idx].get_width() * boom_scale),
                                int(boom_img[boom_frame_idx].get_height() * boom_scale)
                            )
                        )
                        rect = boom_img_scaled.get_rect(center=monster_positions[idx])
                        screen.blit(boom_img_scaled, rect)
                    # Cek durasi efek
                    if pygame.time.get_ticks() - effect["timer"] > 250:
                        effect["active"] = False
            # Hapus efek yang sudah tidak aktif
            boom_effects = [e for e in boom_effects if e["active"]]

        # Tampilkan energi party
        font_energy = pygame.font.Font(None, 40)
        energy_text = font_energy.render(f"ENERGI: {energy}", True, GOLD)
        screen.blit(energy_text, (WIDTH // 2 - 60, 30))

        pygame.display.update()

    pygame.quit()
