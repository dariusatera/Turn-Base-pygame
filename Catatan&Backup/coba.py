import pygame
from config import WIDTH, HEIGHT
from Battle2 import Battle2 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Battle")

while True:
    result = Battle2(screen)
    if result == "QUIT":
        break
    

pygame.quit()