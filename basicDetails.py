import os
import pygame
from pygame.locals import *

CURRENT_DIR = os.path.dirname(__file__)
TEXTURES_PATH = os.path.join(CURRENT_DIR, '_textures')
LEVELS_PATH = os.path.join(CURRENT_DIR, '_levels')

WALL_SYMBOL = "("
FONE_SYMBOL = "["

FPS = 60
WIN_SIZE = (1000, 1000)
CELL_SIZE = 50

BOSS_INFO = 0   # x,y,hp
PLAYER_SPRITE_INFO = 1

GAME_OVER = True
WIN = False
GAME_IN_PROCESS = None


def load_image(img, colorkey=None):
    try:
        image = pygame.image.load(img)
    except Exception:
        print('Картинка не нашлась')
        image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        image.fill(pygame.Color('red'))
        return image

    if colorkey is None:
        image.convert()
    else:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        image.convert_alpha()

    return image