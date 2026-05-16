from menu1 import main_game_menu
from stage1 import stage1
from stage2 import stage2
from stage3 import stage3
from Battle1 import Battle1
from Battle2 import Battle2
from Battle3 import Battle3 
import pygame
from config import WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    result = main_game_menu(screen)
    if result == "QUIT":
        break 
    elif result == "STAGE1":
        result2 = stage1(screen)
        if result2 == "QUIT":
            break
        result3 = Battle1(screen)
        if result3 == "QUIT":
            break
        elif result3 == "WIN":
            # lanjut ke stage berikutnya
            result4 = stage2(screen)
            print("result4 dari stage2:", result4)
            if result4 == "QUIT":
                break
            elif result4 == "BATTLE2":
                print("Masuk ke Battle2")
                result5 = Battle2(screen)
                if result5 == "QUIT":
                    break
                elif result5 == "WIN":
                    # lanjut ke stage berikutnya atau ending
                    result6 = stage3(screen)
                    print("result6 dari stage3:", result6)
                    if result6 == "QUIT":
                        break
                    elif result6 == "BATTLE3":
                        print("Masuk ke Battle3")
                        result7 = Battle3(screen)
                        if result7 == "QUIT":
                            break
                        elif result7 == "WIN":
                            # tampilkan layar kemenangan atau kembali ke menu
                            result = main_game_menu(screen)
                            if result == "QUIT":
                                break
                        elif result7 == "GAMEOVER":
                            # tampilkan layar game over atau kembali ke menu
                            result = main_game_menu(screen)
                            if result == "QUIT":
                                break
                elif result5 == "GAMEOVER":
                    # tampilkan layar game over atau kembali ke menu
                    result = main_game_menu(screen)
                    if result == "QUIT":
                        break
        elif result3 == "GAMEOVER":
            # tampilkan layar game over atau kembali ke menu
            result = main_game_menu(screen)
            if result == "QUIT":
                break
        
        
pygame.quit()
