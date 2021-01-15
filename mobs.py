import pygame
from pygame.locals import *
import os
from random import choice, randint

from basicDetails import *


def check_cooldown(data):
    if pygame.time.get_ticks() - data.last_survey >= data.cooldown:
        data.last_survey = pygame.time.get_ticks()
        return True
    return False


class Boss(pygame.sprite.Sprite):
    group = None
    img = os.path.join(TEXTURES_PATH, 'BOSS\\BOSS.png')

    def __init__(self, x, y, hp):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.health_point = hp
        self.attack_list = [fire_ball, snow_ball]

    def create_attack(self, player):
        check = choice([True, False])
        #print(check)
        if check:
            attack = choice(self.attack_list)
            if check_cooldown(attack):
                attack_rect = load_image(attack.img, (255, 255, 255)).get_rect()
                x_pos = randint(self.rect.x + attack_rect.width, self.rect.x + self.rect.width - attack_rect.width)
                y_pos = randint(self.rect.y, self.rect.y + self.rect.height)

                gamer_rect = player.rect
                speed_x = 0
                speed_y = 1

                attack_rect = attack_rect.move(x_pos, y_pos)

                if gamer_rect.centerx < attack_rect.centerx:
                    speed_x = -1
                elif gamer_rect.centerx > attack_rect.centerx:
                    speed_x = 1

                side_x = abs(attack_rect.centerx - gamer_rect.centerx)
                side_y = abs(attack_rect.centery - gamer_rect.centery)
                hypotenuse = (side_x * side_x + side_y * side_y) ** 0.5

                speed_x *= attack.attack_speed * (side_x / hypotenuse)
                speed_y *= attack.attack_speed * (side_y / hypotenuse)

                return attack(x_pos, y_pos, int(speed_x), int(speed_y))
        return None

    def update(self, data):
        damage = pygame.sprite.spritecollide(self, data.players_attack, True)
        if bool(data):
            for attack in damage:
                self.health_point -= attack.get_damage()
                print(self.health_point)

        return self.create_attack(data.player)

    def is_dead(self):
        if self.health_point <= 0:
            return True
        return False


class base_mob_attack(pygame.sprite.Sprite):
    group = None

    def __init__(self):
        super().__init__(self.__class__.group)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.speed_x = 0
        self.speed_y = 0
        Sound(self.__class__.sound).play()

    def draw(self, fill, camera):
        fill.blit(self.image, camera)

    def get_damage(self):
        return self.damage

    def update(self, data):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        del_attack = pygame.sprite.spritecollide(self, data.players_attack, True)
        if bool(del_attack):
            for attack in del_attack:
                pygame.sprite.spritecollide(attack, data.mobs_attack, True)


class fire_ball(base_mob_attack):
    img = os.path.join(TEXTURES_PATH, 'fire_ball.png')
    sound = os.path.join(SOUND_PATH, 'snow_ball_sound.wav')
    last_survey = 0
    cooldown = 1000
    attack_speed = 10

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = 10
        print(f"new {self.__class__.__name__}: {x}, {y}; create time: {pygame.time.get_ticks()}")


class snow_ball(base_mob_attack):
    img = os.path.join(TEXTURES_PATH, 'snow_ball.png')
    sound = os.path.join(SOUND_PATH, 'snow_ball_sound.wav')
    last_survey = 0
    cooldown = 10000
    attack_speed = 5

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = 200
        print(f"new {self.__class__.__name__}: {x}, {y}; create time: {pygame.time.get_ticks()}")