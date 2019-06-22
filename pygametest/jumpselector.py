import pygame
from pygame.locals import *
from iterator import set_iterator
from utils import EventTimer
from utils import RenderingOperator
from const import *
import json
import sys
import time

class JumpSelector():
    def __init__(self, render):
        self.render = render
        self.screen = render.screen
        self.sysfont = render.sysfont
        self.basepos = POS_JUMPBASE
        self.mergin = TILE_MERGIN
        self.tilesize = TILE_SIZE

        self.load_convert()
        self.set_karimoji()

    def load_convert(self, path="../data/convert.json"):
        with open(path, "r", encoding="utf-8") as fcon:
            self.cor_let_table = json.load(fcon)

    def set_karimoji(self):
        mojis = "あいうえかきくけさしすせたちつてなにぬねはひふへ"
        self.karimoji = [mojis[4 * i:4 * i + 4] for i in range(6)]

    def draw_square(self, x, y, color=BACKGROUND):
        mergin = self.mergin
        size = self.tilesize
        outside = pygame.Rect(x, y, size, size)
        inside = pygame.Rect(x + mergin / 2,
                             y + mergin / 2,
                             size - mergin,
                             size - mergin)

        pygame.draw.rect(self.screen, BLACK, outside)
        pygame.draw.rect(self.screen, color, inside)

    def draw_mojisquare(self, x: int, y: int, moji: str, selected: bool=False):
        # 上から塗る順番を間違えないようにしましょう
        # 四角→文字の順番で
        if selected:
            self.draw_square(x, y, color=COLOR_SELECTED)
        else:
            self.draw_square(x, y)
        text_letter = self.sysfont.render(moji, True, BLACK)
        self.screen.blit(text_letter, (x, y))

    def draw_fillsquare(self, x, y, color):
        # 塗りつぶした正方形を出現させるだけ
        # 湧けるほどでないかもだけど一応
        square = pygame.Rect(x, y, self.tilesize, self.tilesize)
        pygame.draw.rect(self.screen, color, square)

    def draw_tiles(self):
        size = self.tilesize
        # [["あ", "い", "う" "え"], ["か", "き", "く", "け"], ...]
        colors = [BLUE, ORANGE, WHITE, RED, YELLOW, GREEN]
        xbase, ybase = self.basepos
        x, y = self.basepos
        for i in range(6):
            x = xbase
            color = colors[i]
            self.draw_fillsquare(x, y, color)
            x += size
            for j in range(4):
                self.draw_mojisquare(x, y, self.karimoji[i][j])
                x += size
            y += size

    def pickup_tile(self, tilex, tiley):
        x, y = self.basepos
        size = self.tilesize
        mojis = "あいうえかきくけさしすせたちつてなにぬねはひふへ"
        self.draw_mojisquare(x + size * (tilex + 1),
                             y + size * tiley,
                             self.karimoji[tiley][tilex],
                             selected=True)

    def draw_selected_moji(self, n_slide: int, moji: str):
        if moji == "":
            return

        x, y = POS_UNDERBAR
        x += n_slide * BAR_STRIDE
        y -= 25
        text_letter = self.sysfont.render(moji, True, WHITE)
        self.screen.blit(text_letter, (x, y))
        self.draw_underbar(n_slide, blink=False)

    def draw_underbar(self, n_slide: int, blink: bool=True):
        x, y = POS_UNDERBAR
        x += n_slide * BAR_STRIDE
        bar = pygame.Rect(x, y, BAR_LENGTH, 2)
        t_now = pygame.time.get_ticks()
        color = WHITE
        if (t_now // 500) % 2 == 0 and blink:
            color = BACKGROUND

        pygame.draw.rect(self.screen, color, bar)


    def mainloop(self):
        print("jump into letter selector.")
        right_end = 3
        bottom_end = 5
        tilex, tiley = 0, 0
        cur_mojinum = 0
        selected = []
        while(True):
            self.draw_tiles()
            self.pickup_tile(tilex, tiley)
            for idx, sel_moji in enumerate(selected):
                self.draw_selected_moji(idx, sel_moji)
            if cur_mojinum < 2:
                self.draw_underbar(cur_mojinum)
            pygame.display.update()

            if cur_mojinum == 2:
                break

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    ekey = event.key
                    if ekey == K_LEFT:
                        if tilex > 0:
                            tilex -= 1
                    elif ekey == K_RIGHT:
                        if tilex < right_end:
                            tilex += 1
                    elif ekey == K_UP:
                        if tiley > 0:
                            tiley -= 1
                    elif ekey == K_DOWN:
                        if tiley < bottom_end:
                            tiley += 1


                    elif ekey == K_RETURN:
                        cur_mojinum += 1
                        selected.append(self.karimoji[tiley][tilex])


        pygame.time.wait(1000)
        return "".join(selected)

