import pygame
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK,  GREEN, GREY # Impor dari config.py
from LogikaPertarungan import karakter , Slayer, Mage, Healer, Monster, party, stages, turn_order
pygame.init()


# Fungsi untuk menampilkan pertarungan 
def Slayer(screen):
    slayer_pos = (WIDTH // 8, HEIGHT // 2 + 200)  
    slayer_radius = 40
    SLAYER_COLOR = (WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Keluar dari loop dan program

        screen.fill(BLACK)
        pygame.draw.circle(screen, SLAYER_COLOR, slayer_pos, slayer_radius)
        pygame.display.update()  # <-- Pindahkan ke dalam loop

    return "QUIT"



def Mage(screen):
    mage_pos = (WIDTH // 8 + 80, HEIGHT // 2 + 200)  
    mage_radius = 40
    MAGE_COLOR = (WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Keluar dari loop dan program

        screen.fill(BLACK)
        pygame.draw.circle(screen, MAGE_COLOR, mage_pos, mage_radius)
        pygame.display.update()  # <-- Pindahkan ke dalam loop

    return "QUIT"



def Healer(screen):
    healer_pos = (WIDTH // 8 + 160, HEIGHT // 2 + 200)  
    healer_radius = 40
    HEALER_COLOR = (WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Keluar dari loop dan program

        screen.fill(BLACK)
        pygame.draw.circle(screen, HEALER_COLOR, healer_pos, healer_radius)
        pygame.display.update()  # <-- Pindahkan ke dalam loop

    return "QUIT"



#================BUAT BAR HP========================
def draw_hp_bar(surface, character, x, y, width, height=10):
    """
    Menggambar bar HP untuk karakter di layar Pygame.

    Args:
        surface (pygame.Surface): Permukaan tempat bar HP akan digambar.
        character (karakter): Objek karakter yang HP-nya akan ditampilkan.
        x (int): Koordinat X sudut kiri atas bar HP.
        y (int): Koordinat Y sudut kiri atas bar HP.
        width (int): Lebar maksimum bar HP (misalnya 80 piksel).
        height (int): Tinggi bar HP (default 10 piksel).
    """
    # Warna bar HP
    BAR_COLOR_BACKGROUND = GREY
    BAR_COLOR_FILL = GREEN

    # Pastikan HP tidak negatif
    current_hp = max(0, character.hp)

    # Hitung rasio HP saat ini terhadap HP maksimum
    hp_ratio = current_hp / character.MXhp

    # Hitung lebar bar HP yang terisi
    current_bar_width = int(width * hp_ratio)

    # Gambar background bar HP (selalu lebar penuh)
    background_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, BAR_COLOR_BACKGROUND, background_rect)

    # Gambar bar HP yang terisi
    fill_rect = pygame.Rect(x, y, current_bar_width, height) 
    pygame.draw.rect(surface, BAR_COLOR_FILL, fill_rect)

    # (Opsional) Tambahkan border untuk bar HP agar lebih terlihat
    pygame.draw.rect(surface, BLACK, background_rect, 1) # Tebal border 1 piksel
    


def all_party(screen):
    from LogikaPertarungan import party

    positions = [
        (WIDTH // 10, HEIGHT // 2 + 200),
        (WIDTH // 10 + 90, HEIGHT // 2 + 200),
        (WIDTH // 10 + 180, HEIGHT // 2 + 200)
    ]
    radius = 40
    
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        for idx, character in enumerate(party): # enumerate untuk mendapatkan indeks party atau barisan party dari file LogikaPertarungan.py
            
            # Menggambar lingkaran untuk setiap karakter
            pygame.draw.circle(screen, WHITE, positions[idx], radius)
            
            # Menggambar bar HP untuk setiap karakter
            bar_x = positions[idx][0] - 40  # Sesuaikan agar bar rata tengah dengan lingkaran
            bar_y = positions[idx][1] + radius + 20  # 10 piksel di bawah lingkaran
            draw_hp_bar(screen, character, bar_x, bar_y, 80, 10)
        pygame.display.update()

    return "QUIT"