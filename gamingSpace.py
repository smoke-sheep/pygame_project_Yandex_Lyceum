import pygame
import os

from basicDetails import load_image, TEXTURES_PATH


# класс блока стены(твердого)
class wallBlock(pygame.sprite.Sprite):
    group = None
    base_img = os.path.join(TEXTURES_PATH, 'creature.png')

    def __init__(self, x, y):
        super().__init__(wallBlock.group)
        self.image = load_image(self.__class__.base_img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def get_cord(self):
        return self.rect.x, self.rect.y

    def update(self, data):
        # проверка столкновений снарядов со стенами
        pygame.sprite.spritecollide(self, data.players_attack, True)
        pygame.sprite.spritecollide(self, data.mobs_attack, True)


# класс фонового блока
class foneBlock(pygame.sprite.Sprite):
    group = None
    base_img = os.path.join(TEXTURES_PATH, 'creature.png')

    def __init__(self, x, y):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.base_img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def get_cord(self):
        return self.rect.x, self.rect.y
