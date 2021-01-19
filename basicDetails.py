import os
import pygame
from pygame.mixer import music as sounds_player
from pygame.mixer import Sound
from pygame.locals import *

CURRENT_DIR = os.path.dirname(__file__)
SOUND_PATH = os.path.join(CURRENT_DIR, '_sounds')
MUSIC_PATH = os.path.join(CURRENT_DIR, '_music')
TEXTURES_PATH = os.path.join(CURRENT_DIR, 'Sprites')
PLAYER_SKINS = os.path.join(TEXTURES_PATH, 'Player')
LEVELS_PATH = os.path.join(CURRENT_DIR, '_levels')

WALL_SYMBOL = "("
FONE_SYMBOL = "["

FPS = 60


# получение размеров экрана
def window_init():
    from tkinter import Tk
    temp = Tk()
    MONITOR_SIZE = temp.winfo_screenwidth(), temp.winfo_screenheight()
    temp.destroy()
    del temp
    return MONITOR_SIZE


#WIN_SIZE = window_init()
WIN_SIZE = (1000, 1000)
CELL_SIZE = 50

SOUND_LEVEL = 0.2   # громкость звука

BOSS_INFO = 0   # x,y,hp
PLAYER_SPRITE_INFO = 1

GAME_OVER = True
WIN = False
GAME_IN_PROCESS = None


# функция загрузки изображения
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
