import pygame
from basicDetails import *


class atack(pygame.sprite.Sprite):
    group = None

    def __init__(self, x, y):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.img, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


class base_player_attack(pygame.sprite.Sprite):
    group = None

    def __init__(self):
        super().__init__(self.__class__.group)
        Sound(self.__class__.sound).play()

    def __str__(self):
        return f"x={self.rect.x},y={self.rect.y}"

    def get_damage(self):
        return self.damage


class basic_bullet(base_player_attack):
    img = os.path.join(TEXTURES_PATH, 'atack.png')
    sound = os.path.join(SOUND_PATH, 'basic_bullet_sound.wav')

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 5

        self.damage = 10

    def update(self, data):
        self.rect.y -= self.speed


class wizard_road_sphere(base_player_attack):
    img = os.path.join(TEXTURES_PATH, 'wizard_road_sphere.png')
    sound = os.path.join(SOUND_PATH, 'wizard_road_sphere_sound.wav')

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 10

        self.damage = 100

    def update(self, data):
        self.rect.y -= self.speed