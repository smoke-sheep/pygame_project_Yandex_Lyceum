import pygame
from pygame.locals import *
import os
from random import choice, randint

from basicDetails import *
from informBarModule import helthPointBar


# проверка кулдауна атаки
def check_cooldown(data):
    if pygame.time.get_ticks() - data.last_survey >= data.cooldown:
        data.last_survey = pygame.time.get_ticks()
        return True
    return False


# класс босса
class Boss(pygame.sprite.Sprite):
    group = None    # группа спрайта
    img = os.path.join(TEXTURES_PATH, 'BOSS\\BOSS.png')     # путь к спрайту босса

    def __init__(self, x, y, hp):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.health_point = hp  # запись количества здоровья
        self.health_point_bar = helthPointBar(self.rect.width, self.health_point)   # создание линейки жизни
        self.attack_list = [fire_ball, snow_ball]   # список возможных атак

    # функция генерации атаки
    def create_attack(self, player):
        check = choice([True, False])
        if check:
            attack = choice(self.attack_list)   # выбор типа атаки
            # проверка кулдауна атаки
            if check_cooldown(attack):
                attack_rect = load_image(attack.img, (255, 255, 255)).get_rect()    # получение квадрата атаки

                # получение случайной позиции спауна атаки
                # атака спауниться в пределах босса, не выходит за него и не пересекаеться со стенами
                x_pos = randint(self.rect.x + attack_rect.width, self.rect.x + self.rect.width - attack_rect.width)
                y_pos = randint(self.rect.y, self.rect.y + self.rect.height)

                gamer_rect = player.rect    # получение квадрата игрока
                speed_x = 0     # переменная, отвечающая за скорость по x
                speed_y = 1     # переменная, отвечающая за скорость по y

                attack_rect = attack_rect.move(x_pos, y_pos)    # получение квадрата выбранной атаки

                # определение направления полета снаряда
                if gamer_rect.centerx < attack_rect.centerx:
                    speed_x = -1
                elif gamer_rect.centerx > attack_rect.centerx:
                    speed_x = 1

                # рассчет частей прямоугольного теругольника(длины катета по x, длины катета по y, гипотенуза)
                side_x = abs(attack_rect.centerx - gamer_rect.centerx)
                side_y = abs(attack_rect.centery - gamer_rect.centery)
                hypotenuse = (side_x * side_x + side_y * side_y) ** 0.5

                # рассчет скорости по разным осям
                # рассчет происходит через триганоетрические функции sin, cos
                speed_x *= attack.attack_speed * (side_x / hypotenuse)
                speed_y *= attack.attack_speed * (side_y / hypotenuse)

                return attack(x_pos, y_pos, int(speed_x), int(speed_y))     # создание атаки
        return None

    def update(self, data):
        damage = pygame.sprite.spritecollide(self, data.players_attack, True)   # проверка столкновений снаряда игрока с боссом
        # есть ли столкновения
        if bool(data):
            for attack in damage:
                self.health_point -= attack.get_damage()    # получение урона

        # проверка на существование босса
        if not self.is_dead():
            self.health_point_bar.update(self.rect.x, self.rect.y, self.health_point)   # обновление прямоугольника жизни

        return self.create_attack(data.player)  # создание атаки

    # отрисовка
    def draw(self, fill, camera):
        fill.blit(self.image, camera.apply(self))   # отрисовка босса
        self.health_point_bar.draw(fill, camera)    # отрисовка полоски жизни

    # проверка на существование
    def is_dead(self):
        if self.health_point <= 0:
            return True
        return False


# базовая атака босса
class base_mob_attack(pygame.sprite.Sprite):
    group = None    # группа спрайтов

    def __init__(self):
        super().__init__(self.__class__.group)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.speed_x = 0
        self.speed_y = 0
        Sound(self.__class__.sound).play()  # воспроизведение звука спауна атаки

    # отрисовка атаки
    def draw(self, fill, camera):
        fill.blit(self.image, camera)

    # получение урона атаки
    def get_damage(self):
        return self.damage

    # обновление атаки
    def update(self, data):
        # обновления положения атаки
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # проверка столкновения с другими атаками
        del_attack = pygame.sprite.spritecollide(self, data.players_attack, True)   # получение столкновений атак
        if bool(del_attack):
            for attack in del_attack:
                pygame.sprite.spritecollide(attack, data.mobs_attack, True)     # удаление данной атаки


class fire_ball(base_mob_attack):
    img = os.path.join(TEXTURES_PATH, 'fire_ball.png')
    sound = os.path.join(SOUND_PATH, 'snow_ball_sound.wav')
    last_survey = 0     # время последней атаки
    cooldown = 1000     # кулдаун атаки
    attack_speed = 10   # скорость атаки

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = 10    # урон атаки


class snow_ball(base_mob_attack):
    img = os.path.join(TEXTURES_PATH, 'snow_ball.png')
    sound = os.path.join(SOUND_PATH, 'snow_ball_sound.wav')
    last_survey = 0     # время последней атаки
    cooldown = 10000    # кулдаун атаки
    attack_speed = 5    # скорость атаки

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = 200   # урон атаки