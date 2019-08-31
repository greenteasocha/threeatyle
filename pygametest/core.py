import pygame
from pygame.locals import *
from iterator import set_iterator
from utils import EventTimer
from utils import RenderingOperator
from jumpselector import JumpSelector
import const
from const import *
import sys
import time

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("3style Trainer ver. 0.1.0")

    sysfont = pygame.font.SysFont("Consolas", 20)
    sysfont = pygame.font.Font("../data/font/natumeosmall.ttf", 20)
    resetfont = pygame.font.SysFont("Consolas", 15)
    fonts = {"sysfont": sysfont,
             "resetfont": resetfont}

    # set modules
    render = RenderingOperator(fonts, screen)
    e_timer = EventTimer(render)
    jump_selector = JumpSelector(render)
    alg_iterator = set_iterator(shuffle=False)

    # initial render
    screen.fill(const.BACKGROUND)
    pygame.display.update()

    # get initial letter
    former_letter, former_time = "", ""
    letter, alg, idx = alg_iterator.__next__()
    besttime, lasttime = alg_iterator.get_records(letter)
    print(alg)

    # 手順見せるかのフラグ
    show_alg = False

    while (True):
        # テキスト描画部分の準備
        screen.fill(BACKGROUND)
        render.set_former(former_letter, former_time)
        render.set_alg(alg, str(idx), letter, besttime, lasttime)
        # 描画
        render.draw_former()
        show_alg = alg_iterator.check_state(alg)
        if show_alg:
            render.draw_alg_rec()
        else:
            render.draw_letteronly()
        render.draw_reset(const.POS_RESET)
        render.draw_jump()
        render.draw_prevnext()
        jump_selector.draw_tiles()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == const.KEY_TIMER:
                    e_timer.start_decision()  # 一定時間押されたかを検知、必要ならタイマーモードへ
                    if e_timer.is_measured:
                        pygame.time.wait(200)
                        print("GET: last measured time is {}ms".format(e_timer.last_measured))
                        # タイマーモードへ移行した場合、測定したタイムを記録する
                        former_letter, former_time = letter, str(e_timer.last_measured)
                        alg_iterator.set_records(letter, e_timer.last_measured)
                        alg_iterator.dump_records()
                        letter, alg, idx = alg_iterator.__next__()
                        besttime, lasttime = alg_iterator.get_records(letter)

                    print(alg)

                elif event.key == K_a:
                    # 次の手順へ
                    if alg_iterator.idx > 1:
                        print(alg_iterator.idx)
                        alg_iterator.idx -= 2  # ここ若干ハードコーディングで危険
                        letter, alg, idx = alg_iterator.__next__()
                        besttime, lasttime = alg_iterator.get_records(letter)

                elif event.key == K_d:
                    # 前の手順へ
                    letter, alg, idx = alg_iterator.__next__()
                    besttime, lasttime = alg_iterator.get_records(letter)

                elif event.key == K_s:
                    # 手順表示/非表示の切り替え
                    state = alg_iterator.change_state(alg)
                    show_alg = state

                elif event.key == K_r:
                    # 現在表示されているタイムの消去
                    if letter in alg_iterator.besttime:
                        alg_iterator.delete_records(letter)
                        besttime, lasttime = alg_iterator.get_records(letter)
                        render.paint_reset(const.POS_RESET)

                elif event.key == K_j:
                    assigned = jump_selector.mainloop()
                    try:
                        alg_iterator.jump_letter(assigned)
                    except:
                        print("Caught noletter error.")
                        render.draw_peke(PEKE_BEG, PEKE_END)
                    letter, alg, idx = alg_iterator.__next__()
                    besttime, lasttime = alg_iterator.get_records(letter)


if __name__ == "__main__":
    main()