from basicDetails import *


class Game_over(pygame.sprite.Sprite):
    group = None
    img = os.path.join(TEXTURES_PATH, 'gameover.png')

    def __init__(self):
        super().__init__(self.__class__.group)
        self.image = load_image(self.__class__.img)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(-WIN_SIZE[0], 0)
        self.speed = 200 // FPS
        # Object.group.add(self)
        # self.add(Object.group)

    def update(self):
        print(self.rect.x, self.rect.y)
        if self.rect.x != 0:
            self.rect.x += self.speed
