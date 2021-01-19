import pygame as pg
from pygame.locals import *
import os

from basicDetails import *
from playerElements.CameraModule import camera_configure, Camera
from playerElements.Atacks import base_player_attack
from playerElements.weapoints import baseWeapon, blackGun, wizardRoad
from informBarModule import helthPointBar


# класс игрока
class Player(pg.sprite.Sprite):
    group = None    # группа

    # изображения
    move_straight = None
    move_left = None
    move_right = None
    move_back = None

    def __init__(self, x, y):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.move_straight, -1)   # загрузка начального изображения
        self.rect = self.image.get_rect()   # получение прямоугольника изображения
        self.rect = self.rect.move(x, y)    # перенос прямогульника на позицию спауна
        self.speed = 10     # скорость персонажа
        self.health_point = 500     # очки жизни персонажа

        self.events = None  # события, которые передаються игроку

        self.weapoint_pos = (30, 30)    # позция оружия на квадрает персонажа
        # рассчет координат оружия на основном квадрате поля
        x = self.rect.x + self.weapoint_pos[0]
        y = self.rect.y + self.weapoint_pos[1]

        self.weapons = [blackGun(x, y), wizardRoad(x, y)]  # список оружия
        self.active_weapon = 0  # номер активного оружия(индекс в списке оружия)

        self.health_point_bar = helthPointBar(self.rect.width, self.health_point) # создание линейки здоровья

    # записаь новых событий
    def write_events(self, events):
        self.events = events

    # обработчик событий
    def processing_events(self):
        out_data = None
        if not self.events is None:
            for event in self.events:
                if event.type == KEYUP:
                    # если нажать пробел, будет осуществлен выстрел
                    if event.key == K_SPACE:
                        out_data = self.weapons[self.active_weapon].attack()    # создаеться атака оружия
                    # если нажата F то происходит смещение оружия
                    elif event.key == K_f:
                        self.active_weapon -= 1
                        if self.active_weapon < 0:
                            self.active_weapon = len(self.weapons) - 1
                    # если нажата G то происходит смещение оружия
                    elif event.key == K_g:
                        self.active_weapon += 1
                        if self.active_weapon >= len(self.weapons):
                            self.active_weapon = 0

            self.events = None  # обнуление списка событий
        return out_data

    # обновление персонажа
    def update(self, data):
        keys = pg.key.get_pressed()
        left = keys[K_a] or keys[K_LEFT]
        right = keys[K_d] or keys[K_RIGHT]
        up = keys[K_w] or keys[K_UP]
        down = keys[K_s] or keys[K_DOWN]

        if up == down:
            speed_y = 0
        elif up:
            speed_y = -self.speed
            self.image = load_image(self.__class__.move_back, -1)
        else:
            speed_y = self.speed
            self.image = load_image(self.__class__.move_straight, -1)
        self.rect.y += speed_y

        if left == right:
            speed_x = 0
        elif left:
            speed_x = -self.speed
            self.image = load_image(self.__class__.move_left, -1)
        else:
            speed_x = self.speed
            self.image = load_image(self.__class__.move_right, -1)
        self.rect.x += speed_x

        # проверка на столкновение со стенами
        if pg.sprite.spritecollide(self, data.walls, False) or pg.sprite.spritecollide(self, data.mobs, False):
            self.rect.x -= speed_x
            self.rect.y -= speed_y

        # проверка на столкновение с атаками босса
        damage = pg.sprite.spritecollide(self, data.mobs_attack, True)  # получение списка столкнувшихся с персонажем атак
        if bool(damage):
            for attack in damage:
                self.health_point -= attack.get_damage()    # получение дамага

        # рассчет координат оружия на основном квадрате поля
        x = self.rect.x + self.weapoint_pos[0]
        y = self.rect.y + self.weapoint_pos[1]
        self.weapons[self.active_weapon].update(x, y)   # обновление положения оружия на основном поле

        # проверка на существование персонажа, могут возникнуть ошибки с преобразованием значений, если не проверить
        if not self.is_dead():
            self.health_point_bar.update(self.rect.x, self.rect.y, self.health_point)   # обновление прямоугольника жизни

        return self.processing_events()     # обработка событий

    # отрисовка
    def draw(self, fill, camera):
        fill.blit(self.image, camera.apply(self))   # отрисовка персонажа
        self.health_point_bar.draw(fill, camera)    # отрисовка прямоугольника жизни
        self.weapons[self.active_weapon].draw(fill, camera)     # отрисовка оружия

    # проверка: жив ли персонаж
    def is_dead(self):
        if self.health_point <= 0:
            return True
        return False
