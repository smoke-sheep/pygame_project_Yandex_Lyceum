import pygame
from basicDetails import *


# базовая атака персонажа
class base_player_attack(pygame.sprite.Sprite):
    group = None    # группа спрайтов

    def __init__(self):
        super().__init__(self.__class__.group)
        Sound(self.__class__.sound).play()  # воспроизведение звука патрона

    def __str__(self):
        return f"x={self.rect.x},y={self.rect.y}"

    # получение урона атаки
    def get_damage(self):
        return self.damage

    # обновление позиции
    def update(self, data):
        self.rect.y -= self.speed


class basic_bullet(base_player_attack):
    img = os.path.join(TEXTURES_PATH, 'atack.png')
    sound = os.path.join(SOUND_PATH, 'basic_bullet_sound.wav')  # звук спауна атаки

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 5  # скорость атаки

        self.damage = 10    # урон, наносимы атакой


class wizard_road_sphere(base_player_attack):
    img = os.path.join(TEXTURES_PATH, 'wizard_road_sphere.png')
    sound = os.path.join(SOUND_PATH, 'wizard_road_sphere_sound.wav')    # звук спауна атаки

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 10     # скорость атаки

        self.damage = 100   # урон атаки
