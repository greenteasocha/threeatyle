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
    resetfont = pygame.font.SysFont("Consolas", 15)
    fonts = {"sysfont": sysfont,
             "resetfont": resetfont}

    render = RenderingOperator(fonts, screen)
    e_timer = EventTimer(render)
    alg_iterator = set_iterator()

    # initial render
    screen.fill(const.BACKGROUND)
    pygame.display.update()

    # get initial letter
    letter, alg, idx = alg_iterator.__next__()
    besttime, lasttime = alg_iterator.get_records(letter)
    print(alg)

    while (True):
        # テキスト描画部分
        screen.fill(BACKGROUND)
        render.set_alg(alg, str(idx), letter, besttime, lasttime)
        render.draw_alg_rec()
        render.draw_reset(const.POS_RESET)
        render.draw_prevnext()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    e_timer.start_decision()  # 一定時間押されたかを検知、必要ならタイマーモードへ
                    if e_timer.is_measured:
                        pygame.time.wait(200)
                        print("GET: last measured time is {}ms".format(e_timer.last_measured))
                        # タイマーモードへ移行した場合、測定したタイムを記録する
                        alg_iterator.set_records(letter, e_timer.last_measured)
                        alg_iterator.dump_records()
                        letter, alg, idx = alg_iterator.__next__()
                        besttime, lasttime = alg_iterator.get_records(letter)

                    print(alg)

                if event.key == K_a:
                    if alg_iterator.idx > 1:
                        print(alg_iterator.idx)
                        alg_iterator.idx -= 2  # ここ若干ハードコーディングで危険
                        letter, alg, idx = alg_iterator.__next__()
                        besttime, lasttime = alg_iterator.get_records(letter)

                if event.key == K_d:
                    letter, alg, idx = alg_iterator.__next__()
                    besttime, lasttime = alg_iterator.get_records(letter)

                if event.key == K_r:
                    if letter in alg_iterator.besttime:
                        del alg_iterator.besttime[letter]
                        del alg_iterator.lasttime[letter]
                        besttime, lasttime = alg_iterator.get_records(letter)
                        render.paint_reset(const.POS_RESET)


if __name__ == "__main__":
    main()