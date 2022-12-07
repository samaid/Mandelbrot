import os
import pygame as pg

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 800, 600
FPS = 60

OFFSET_X = 1.4*DISPLAY_W//2
OFFSET_Y = DISPLAY_H//2
ZOOM = 2.5/DISPLAY_H

MAX_ITER = 30


def set_display():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    surface = pg.display.set_mode(DISPLAY_RES, pg.SCALED)
    clock = pg.time.Clock()

    return surface, clock


def initialize():
    surface, clock = set_display()
    return surface, clock
