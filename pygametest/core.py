import pygame
from pygame.locals import *
from iterator import set_iterator
from utils import EventTimer
from utils import RenderingOperator
import const
import sys
import time

SCREEN_SIZE = (600, 400)
BACKGROUND = (153, 204, 0)
BLACK = (0, 0, 0)
KEY_TIMER = K_LEFT

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("3style Trainer ver. 0.1.0")

    sysfont = pygame.font.SysFont("Consolas", 20)

    render = RenderingOperator(sysfont, screen)
    e_timer = EventTimer(screen, sysfont, render)
    alg_iterator = set_iterator()

    # initial render
    screen.fill(const.BACKGROUND)
    pygame.display.update()

    # get initial letter
    letter, alg, idx = alg_iterator.__next__()
    print(alg)

    while (True):
        # テキスト描画部分
        # screen.blit(hello1, (20, 50))
        screen.fill(BACKGROUND)
        render.set_alg(alg, str(idx), letter)
        render.draw_alg()
        render.draw_reset(100,100,100,100,10)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    e_timer.start_decision()
                    if e_timer.is_measured:
                        print("GET: last measured time is {}ms".format(e_timer.last_measured))
                        alg_iterator.set_record(letter, e_timer.last_measured)
                        alg_iterator.dump_record()
                        letter, alg, idx = alg_iterator.__next__()

                    print(alg)



if __name__ == "__main__":
    main()