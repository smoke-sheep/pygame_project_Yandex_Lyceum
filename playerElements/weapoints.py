import pygame
from basicDetails import *
from playerElements.Atacks import basic_bullet, wizard_road_sphere


class baseWeapon(pygame.sprite.Sprite):
    group = None

    def __init__(self):
        super().__init__(self.__class__.group)
        self.last_survey = 0

    def draw(self, fill, camera):
        fill.blit(self.image, camera.apply(self))

    def check_cooldown(self):
        if pygame.time.get_ticks() - self.last_survey >= self.cooldown:
            self.last_survey = pygame.time.get_ticks()
            return True
        return False


class blackGun(baseWeapon):
    img = os.path.join(TEXTURES_PATH, 'black_gun.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.attack_spawn_positional = (5, 5)
        self.cooldown = 100

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def attack(self):
        if self.check_cooldown():
            x = self.rect.x + self.attack_spawn_positional[0]
            y = self.rect.y + self.attack_spawn_positional[1]
            return basic_bullet(x, y)
        return None


class wizardRoad(baseWeapon):
    img = os.path.join(TEXTURES_PATH, 'wizard_road.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(self.__class__.img, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.attack_spawn_positional = (5, 5)
        self.cooldown = 1000

    def update(self, x, y):
        print("move:", x, y)
        self.rect.x = x
        self.rect.y = y

    def attack(self):
        if self.check_cooldown():
            x = self.rect.x + self.attack_spawn_positional[0]
            y = self.rect.y + self.attack_spawn_positional[1]
            return wizard_road_sphere(x, y)
        return None