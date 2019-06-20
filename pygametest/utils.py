import pygame
from pygame.locals import *
from iterator import set_iterator
import const
import sys
import time

SCREEN_SIZE = (600, 400)
BACKGROUND = (153, 204, 0)
BLACK = (0, 0, 0)
KEY_TIMER = K_LEFT

class EventTimer():
    def __init__(self, render):
        self.hold_to_start = 200 # ms
        self.wait_after_measure = 200 # ms
        self.render = render
        self.screen = render.screen
        self.sysfont = render.sysfont
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
                    self.render.draw_alg_rec()
                    pygame.display.update()

    def countup(self):
        t_0 = pygame.time.get_ticks()
        print("Countup start.")

        while(True):
            t_now = pygame.time.get_ticks()
            t_passed = t_now - t_0

            self.screen.fill(BACKGROUND)
            self.render.draw_running(t_passed)
            self.render.draw_alg_rec()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.last_measured = t_passed
                        pygame.time.wait(self.wait_after_measure)
                        print("Here")
                        return


class RenderingOperator():
    def __init__(self, fonts, screen):
        self.fonts = fonts
        self.screen = screen

        self.get_font()

    def get_font(self):
        self.sysfont = self.fonts["sysfont"]
        self.resetfont = self.fonts["resetfont"]

    def set_alg(self,
                alg: str,
                idx: str,
                letter: str,
                best: int,
                last: int
                ):
        self.alg = alg
        self.idx = idx
        self.letter = letter
        self.best = best
        self.last = last

    def draw_alg(self):
        text_alg = self.sysfont.render(self.alg, True, BLACK)
        text_idx = self.sysfont.render(self.idx, True, BLACK)
        text_letter = self.sysfont.render(self.letter, True, BLACK)
        self.screen.blit(text_alg, const.POS_ARG)

    def draw_records(self):
        text_best = self.sysfont.render("BEST TIME     :{}".format(str(self.best)), True, BLACK)
        text_last = self.sysfont.render("LAST MEASURED :{}".format(str(self.last)), True, BLACK)
        self.screen.blit(text_best, const.POS_BEST)
        self.screen.blit(text_last, const.POS_LAST)

    def draw_alg_rec(self):
        self.draw_alg()
        self.draw_records()

    def draw_prevnext(self):
        text_prevnext = self.sysfont.render("< PREV (A)    (D) NEXT >", True, BLACK)
        self.screen.blit(text_prevnext, const.POS_PREVNEXT)

    def draw_ready(self, pos_ready=(20, 50)):
        text_ready = self.sysfont.render("Ready?", True, (255, 0, 0))  # 赤文字へ
        self.screen.blit(text_ready, (20, 50))

    def draw_reset(self, status):
        x, y, xlen, ylen, mergin = status
        outside = pygame.Rect(x, y, xlen, ylen)
        inside = pygame.Rect(x + mergin/2,
                             y + mergin/2,
                             xlen - mergin,
                             ylen - mergin)
        pygame.draw.rect(self.screen, (255, 0, 0), outside)
        pygame.draw.rect(self.screen, BACKGROUND, inside)
        text_reset = self.resetfont.render("RESET? (R)", True, BLACK)
        self.screen.blit(text_reset, (x+10, y+3))

    def paint_reset(self, status):
        x, y, xlen, ylen, mergin = status
        outside = pygame.Rect(x, y, xlen, ylen)
        pygame.draw.rect(self.screen, (255, 0, 0), outside)
        pygame.display.update()
        pygame.time.wait(100)


    def draw_running(self, curtime: int, pos_time=(20, 100)):
        text_running = self.sysfont.render("Running...", True, (0, 0, 0))
        text_curtime = self.sysfont.render(str(curtime / 1000), True, (0, 0, 0))
        self.screen.blit(text_running, (20, 50))
        self.screen.blit(text_curtime, (20, 100))


