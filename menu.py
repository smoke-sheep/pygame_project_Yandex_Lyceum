import pygame
import pygame_menu
from main import Game

player = {
        '1': 'Men',
        '2': 'Women',
        '3': 'Zombie'
    }

active_index = 1

pygame.init()
surface = pygame.display.set_mode((1000, 1000))

def set_difficulty(value, difficulty):
    pass

def start_the_game():
    Game(player[str(active_index)]).run()

def onchange(current_text, index):
    global active_index
    active_index = index

menu = pygame_menu.Menu(1000, 1000, 'Игра',
                       theme=pygame_menu.themes.THEME_ORANGE)

# menu.add_text_input('Имя : ', default='Ваше Имя')
menu.add_selector('Персонаж : ', [('Мужчина', 1), ('Женщина', 2), ('Зомби', 3)], 
    onchange=onchange)
menu.add_button('Играть', start_the_game)
menu.add_button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(surface)