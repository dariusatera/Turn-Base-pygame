import pygame
from config import WIDTH, HEIGHT, BLACK, WHITE, GREEN, GREY, RED, GOLD
from partycode import party, draw_hp_bar
from TomboBattle import battle_tombol  # ambil logika gambarnya saja
from LogikaPertarungan import (
    karakter, Slayer, Mage, Healer, Monster, stages, turn_order, stage_1, stage_2, stage_3
)

pygame.init()

def test1(screen):
    # ======================= Buat Import Suara ============================= #
    pygame.mixer.init()
    SOUND_END_EVENT = pygame.USEREVENT + 1  # Event untuk mendeteksi akhir musik

    pygame.mixer.music.load(r"C:\Codingan\projactG\sound\Battle.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(SOUND_END_EVENT)  # Set event ketika musik selesai

    loop_sound_path = r"C:\Codingan\projactG\sound\Phalanx_Battle_soundtrack.mp3"
    music_playing = False 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle & Party")

    # --- Siapkan font dan tombol seperti di battle_tombol ---
    font_pukul = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)
    font_skill = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)
    font_ulti = pygame.font.Font(r"C:\Codingan\projactG\font\Exquisite Corpse.ttf", 55)

    pukul = font_pukul.render("Pukul", True, WHITE)
    skill = font_skill.render("Skill", True, WHITE)
    ulti = font_ulti.render("CORE", True, WHITE)

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
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\slayer.png").convert_alpha(), 
            (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), 
            (radius*2, radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\healer.png").convert_alpha(), 
            (radius*2, radius*2)
        ),
    ]

    # Load gambar PNG untuk monster (menggunakan gambar mage sebagai placeholder)
    monster_imgs = [
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), 
            (monster_radius*2, monster_radius*2)
        ),
        pygame.transform.scale(
            pygame.image.load(r"C:\Codingan\projactG\Asset\Party\mage.png").convert_alpha(), 
            (monster_radius*2, monster_radius*2)
        ),
    ]

    # Ambil stage pertama dari daftar stages
    monsters = stages[0]

    blink = False
    blink_count = 0
    blink_timer = 0
    blink_target = None

    # ----------------- Variabel Turn-Based ----------------- #
    current_turn_index = 0       # Menunjukkan indeks giliran saat ini
    monster_action_started = False
    monster_action_delay = 1000  # Delay aksi monster (ms)
    monster_action_timer = 0

    # Variabel untuk mengatur aksi player yang sedang memilih target
    player_action_mode = None   # Nilai bisa "pukul", "skill", atau "ulti"

    # Helper: mengambil target hidup dari daftar yang diberikan
    def get_target(target_list):
        for t in target_list:
            if t.is_alive():
                return t
        return None

    # Helper: menghitung ulang urutan giliran berdasarkan karakter hidup
    def get_turns():
        living_party = [p for p in party if p.is_alive()]
        living_monsters = [m for m in monsters if m.is_alive()]
        return turn_order(living_party, living_monsters)

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)  # Batas frame rate 30 FPS
        mouse_pos = pygame.mouse.get_pos()

        # Hitung ulang urutan giliran (hanya karakter hidup)
        turns = get_turns()
        # Kondisi akhir pertempuran:
        if not any(isinstance(c, Monster) for c in turns):
            print("Party menang!")
            running = False
        if not any((not isinstance(c, Monster)) for c in turns):
            print("Monster menang!")
            running = False
        if not turns:
            running = False
            break
        if current_turn_index >= len(turns): # Jika indeks giliran melebihi jumlah karakter, reset ke awal
            current_turn_index = 0
        current_turn = turns[current_turn_index] # Dapatkan karakter saat ini berdasarkan indeks

        # ---------------- Event Handling ---------------- # 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == SOUND_END_EVENT and not music_playing:
                pygame.mixer.music.load(loop_sound_path)
                pygame.mixer.music.play(-1)
                music_playing = True

            # Jika giliran adalah anggota party
            if not isinstance(current_turn, Monster):
                # Jika belum memilih aksi, periksa apakah tombol aksi ditekan
                if player_action_mode is None and event.type == pygame.MOUSEBUTTONDOWN:
                    # Tombol aksi ditekan? Set mode tindakan yang dipilih
                    if pukul_rect.collidepoint(event.pos):
                        print(f"{current_turn.nama} mempersiapkan Basic Attack!")
                        player_action_mode = "pukul"
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "pukul"
                    elif skill_rect.collidepoint(event.pos):
                        print(f"{current_turn.nama} mempersiapkan Skill!")
                        player_action_mode = "skill"
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "skill"
                    elif ulti_rect.collidepoint(event.pos):
                        print(f"{current_turn.nama} mempersiapkan Ultimate!")
                        player_action_mode = "ulti"
                        blink = True
                        blink_count = 0
                        blink_timer = pygame.time.get_ticks()
                        blink_target = "ulti"
                # Jika mode aksi sudah aktif, maka cek apakah player mengklik pada monster untuk memilih target
                elif player_action_mode is not None and event.type == pygame.MOUSEBUTTONDOWN:
                    # Periksa apakah klik berada di atas salah satu monster (hanya yang masih hidup)
                    target_chosen = None
                    for idx, monster in enumerate(monsters):
                        if not monster.is_alive():
                            continue
                        monster_rect = monster_imgs[idx].get_rect(center=monster_positions[idx])
                        if monster_rect.collidepoint(event.pos):
                            target_chosen = monster
                            break
                    if target_chosen:
                        if player_action_mode == "pukul":
                            print(f"{current_turn.nama} melakukan Basic Attack kepada {target_chosen.nama}!")
                            current_turn.BasicAttack(target_chosen)
                        elif player_action_mode == "skill":
                            print(f"{current_turn.nama} menggunakan Skill kepada {target_chosen.nama}!")
                            current_turn.Skill(target_chosen)
                        elif player_action_mode == "ulti":
                            print(f"{current_turn.nama} menggunakan Ultimate kepada {target_chosen.nama}!")
                            current_turn.Ultimate(target_chosen)
                        # Reset mode aksi setelah aksi dijalankan dan lanjut giliran
                        player_action_mode = None
                        current_turn_index += 1

        # ---------------- Aksi Otomatis Monster ---------------- #
        if isinstance(current_turn, Monster):
            if not monster_action_started:
                monster_action_started = True
                monster_action_timer = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - monster_action_timer > monster_action_delay:
                    print(f"{current_turn.nama} (Monster) melakukan Basic Attack!")
                    target = get_target(party)
                    if target:
                        current_turn.BasicAttack(target)
                    else:
                        print("Tidak ada anggota party yang hidup!")
                    monster_action_started = False
                    current_turn_index += 1

        # ---------------- Tampilan layar (Drawing) ---------------- #
        screen.fill(BLACK)

        # Gambar party
        for idx, character in enumerate(party):
            img_rect = character_imgs[idx].get_rect(center=positions[idx])
            screen.blit(character_imgs[idx], img_rect)
            bar_x = positions[idx][0] - 40
            bar_y = positions[idx][1] + radius + 20
            draw_hp_bar(screen, character, bar_x, bar_y, 80, 10)

        # Gambar monster
        for idx, monster in enumerate(monsters):
            img_rect = monster_imgs[idx].get_rect(center=monster_positions[idx])
            screen.blit(monster_imgs[idx], img_rect)
            bar_x = monster_positions[idx][0] - 50
            bar_y = monster_positions[idx][1] + monster_radius + 20
            draw_hp_bar(screen, monster, bar_x, bar_y, 80, 10)

        # Efek blink untuk tombol
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

        # Render tombol, tetap ditampilkan untuk referensi visual
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

        # Gambarkan tombol aksi (meskipun saat ini player dalam mode pemilihan target, tombol tetap terlihat)
        if show_pukul:
            screen.blit(pukul_display, pukul_rect)
        if show_skill:
            screen.blit(skill_display, skill_rect)
        if show_ulti:
            screen.blit(ulti_display, ulti_rect)

        # Tampilkan informasi giliran di pojok kiri atas
        font_turn = pygame.font.Font(None, 36)
        turn_text = font_turn.render(f"Giliran: {current_turn.nama}", True, WHITE)
        screen.blit(turn_text, (20, 20))
        
        # Jika player sedang dalam mode memilih target, beri petunjuk
        if player_action_mode is not None:
            font_target = pygame.font.Font(None, 30)
            target_text = font_target.render("Pilih target musuh", True, RED)
            screen.blit(target_text, (WIDTH //2 - 70, HEIGHT - 50))

        pygame.display.update()

    pygame.quit()