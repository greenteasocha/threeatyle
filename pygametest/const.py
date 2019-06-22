"""
Constant types in Python.
"""
import pygame
from pygame.locals import *

class _const:
    class ConstError(TypeError):
        pass

    def __init__(self):
        # スクリーン
        self.SCREEN_SIZE = (600, 400)
        # 色
        # self.BACKGROUND = (153, 204, 0)
        self.BACKGROUND = (0, 128, 128)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 0, 128)
        self.COLOR_SELECTED = (112, 128, 144)
        # キー
        self.KEY_TIMER = K_SPACE
        # 一つ前の手順
        self.POS_FM = (300, 80)
        self.POS_FMLETTER = (300, 100)
        self.POS_FMRECORD = (360, 100)
        # 現在の手順
        self.POS_LETTER = (300, 180)
        self.POS_IDX = (400, 180)
        self.POS_ARG = (300, 200)
        self.POS_BEST = (300, 220)
        self.POS_LAST = (300, 240)
        # リセットボタン
        self.POS_RESET = (300, 260, 100, 20, 5)
        # PREV/NEZT
        self.POS_PREVNEXT = (300, 290)
        # JUMP 画面
        self.POS_JUMPQ = (20, 210)
        self.POS_JUMPBASE = (100, 200)
        self.TILE_MERGIN = 2  # px
        self.TILE_SIZE = 30
        self.POS_UNDERBAR = (150, 180)
        self.BAR_LENGTH = 20
        self.BAR_STRIDE = 30
        self.PEKE_BEG = (130, 150)
        self.PEKE_END = (210, 190)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__]=_const()