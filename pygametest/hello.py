import pygame
from pygame.locals import *
from iterator import *
import sys

SCREEN_SIZE = (600, 400)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Test Screen.")

    sysfont = pygame.font.SysFont("Consolas", 30)
    hello1 = sysfont.render("Hello, world!", False, (0,0,0))
    hello2 = sysfont.render("Hello, world!", True, (0,0,0))
    hello3 = sysfont.render("Hello, world!", True, (255,0,0), (255,255,0))

    # 手順読み込みイテレータのセット
    alg_iterator = set_iterator()

    while(True):
        screen.fill((153, 204, 0))
        pygame.display.update()
        # テキスト描画部分
        # screen.blit(hello1, (20, 50))
        # screen.blit(hello2, (20, 150))
        # screen.blit(hello3, (20, 250))
        try:
            letter, alg, idx = alg_iterator.__next__()
            idx_drawn = sysfont.render(str(idx), False, (0, 0, 0))
            letter_drawn= sysfont.render(letter, True, (0, 0, 0))
            alg_drawn = sysfont.render(alg, True, (255, 0, 0))
            screen.blit(idx_drawn, (20, 50))
            screen.blit(letter_drawn, (20, 150))
            screen.blit(alg_drawn, (20, 250))
            # alg_iterator.jump_letter(key_input)
        except:
            traceback.print_exc()
            print("all algs over.")
            pygame.quit()

        pygame.display.update()
        
        pygame.time.wait(1000)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()