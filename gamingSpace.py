import pygame
import os

from basicDetails import load_image, TEXTURES_PATH


class baseBlock(pygame.sprite.Sprite):
    group = None
    base_img = os.path.join(TEXTURES_PATH, 'creature.png')

    def __init__(self, x, y):
        super().__init__(baseBlock.group)
        self.image = load_image(baseBlock.base_img, -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


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
        pygame.sprite.spritecollide(self, data.players_attack, True)
        pygame.sprite.spritecollide(self, data.mobs_attack, True)


class foneBlock(baseBlock):
    pass