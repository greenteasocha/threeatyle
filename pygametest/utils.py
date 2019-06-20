import pygame
from pygame.locals import *
from iterator import set_iterator
import sys
import time

SCREEN_SIZE = (600, 400)
BACKGROUND = (153, 204, 0)
BLACK = (0, 0, 0)
KEY_TIMER = K_LEFT

class EventTimer():
    def __init__(self, screen, sysfont, render):
        self.hold_to_start = 200 # ms
        self.wait_after_measure = 200 # ms
        self.screen = screen
        self.sysfont = sysfont
        self.render = render
        self.is_measured = False
        self.last_measured = 100000000
        self.last_letter = ""
        self.last_alg = ""

    def start_decision(self) -> None:
        """
        spaceキーが押されたときにタイマースタートかどうかを判定する
        """
        print("Step into e_timer")

        text_ready = self.sysfont.render("Ready?", False, (0, 0, 0))
        self.screen.blit(text_ready, (20, 50))
        pygame.display.update()

        t_down = pygame.time.get_ticks()
        is_ready = False
        t_hold = 0

        while(True):
            for event in pygame.event.get():
                if event.type == KEYUP:
                    # キーが離されたら(必要であればカウントアップをスタートして)return
                    if is_ready:
                        self.countup()
                        self.is_measured = True
                    else:
                        self.is_measured = False
                    print("Return from e_timer")
                    print("Hold time is {}".format(t_hold))
                    return

            if not is_ready:
                t_hold = pygame.time.get_ticks() - t_down
                if t_hold > self.hold_to_start:
                    # 一定時間計測機―がholdされたら準備完了を示す
                    is_ready = True

                    self.screen.fill(BACKGROUND)
                    self.render.draw_ready()
                    self.render.draw_alg()
                    pygame.display.update()

    def countup(self):
        t_0 = pygame.time.get_ticks()
        print("Countup start.")

        while(True):
            t_now = pygame.time.get_ticks()
            t_passed = t_now - t_0

            self.screen.fill(BACKGROUND)
            self.render.draw_running(t_passed)
            self.render.draw_alg()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.last_measured = t_passed
                        pygame.time.wait(self.wait_after_measure)
                        print("Here")
                        return

class RenderingOperator():
    def __init__(self, sysfont, screen):
        self.sysfont = sysfont
        self.screen = screen

    def set_alg(self,
                alg: str,
                idx: str,
                letter: str,
                pos_alg=(300, 200)):
        self.alg = alg
        self.idx = idx
        self.letter = letter
        self.pos_alg = pos_alg


    def draw_alg(self):
        text_alg = self.sysfont.render(self.alg, True, BLACK)
        text_idx = self.sysfont.render(self.idx, True, BLACK)
        text_letter = self.sysfont.render(self.letter, True, BLACK)
        self.screen.blit(text_alg, self.pos_alg)

    def draw_ready(self, pos_ready=(20, 50)):
        text_ready = self.sysfont.render("Ready?", True, (255, 0, 0))  # 赤文字へ
        self.screen.blit(text_ready, (20, 50))

    def draw_running(self, curtime: int, pos_time=(20, 100)):
        text_running = self.sysfont.render("Running...", True, (0, 0, 0))
        text_curtime = self.sysfont.render(str(curtime / 1000), True, (0, 0, 0))
        self.screen.blit(text_running, (20, 50))
        self.screen.blit(text_curtime, (20, 100))


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("3style Trainer ver. 0.1.0")

    sysfont = pygame.font.SysFont("Consolas", 20)
    text_result = sysfont.render("Result.", True, (255, 0, 0))

    e_timer = EventTimer(screen, sysfont)
    alg_iterator = set_iterator()

    # initial render
    screen.fill(BACKGROUND)
    pygame.display.update()

    # get initial letter
    letter, alg, idx = alg_iterator.__next__()
    text_alg = sysfont.render(alg, True, BLACK)
    text_idx = sysfont.render(str(idx), True, BLACK)
    text_letter = sysfont.render(letter, True, BLACK)

    print(alg)

    while (True):
        # テキスト描画部分
        # screen.blit(hello1, (20, 50))
        screen.blit(text_alg, (300, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    e_timer.start_decision()
                    if e_timer.is_measured:
                        print("GET: last measured time is {}ms".format(e_timer.last_measured))
                    screen.fill(BACKGROUND)
                    pygame.display.update()

if __name__ == "__main__":
    main()