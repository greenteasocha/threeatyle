import pygame
from pygame.locals import *
from iterator import *
import sys
import time

SCREEN_SIZE = (600, 400)
BACKGROUND = (153, 204, 0)
KEY_TIMER = K_LEFT

class EventTimer():
    def __init__(self, screen, sysfont):
        self.hold_to_start = 1000 # ms
        self.screen = screen
        self.sysfont = sysfont
        self.is_measured = False
        self.last_measured = 100000000

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
                    text_ready = self.sysfont.render("Ready?", True, (255, 0, 0)) # 赤文字へ
                    self.screen.blit(text_ready, (20, 50))
                    pygame.display.update()

    def countup(self):
        t_0 = pygame.time.get_ticks()
        print("Countup start.")
        while(True):
            t_now = pygame.time.get_ticks()
            t_passed = t_now - t_0

            self.screen.fill(BACKGROUND)
            text_running = self.sysfont.render("Running...", True, (0, 0, 0))
            text_curtime = self.sysfont.render(str(t_passed/1000), True, (0, 0, 0))
            self.screen.blit(text_running, (20, 50))
            self.screen.blit(text_curtime, (20, 100))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.last_measured = t_passed
                        pygame.time.wait(1000)
                        print("Here")
                        return




def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Test Screen.")

    sysfont = pygame.font.SysFont(None, 80)
    text_ready = sysfont.render("Ready?", False, (0, 0, 0))
    text_running = sysfont.render("Running...", True, (0, 0, 0))
    text_result = sysfont.render("Result.", True, (255, 0, 0))

    e_timer = EventTimer(screen, sysfont)

    while (True):
        screen.fill(BACKGROUND)
        pygame.display.update()
        # テキスト描画部分
        # screen.blit(hello1, (20, 50))
        # screen.blit(hello2, (20, 150))
        # screen.blit(hello3, (20, 250))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    e_timer.start_decision()
                    print("GET: last measured time is {}ms".format(e_timer.last_measured))


if __name__ == "__main__":
    main()