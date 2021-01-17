from basicDetails import *


HElTH_POINT_BAR_SIZE = 10

def transform_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class helthPointBar():
    def __init__(self, size, hp):
        self.rect = pygame.Rect(0, 0, size, HElTH_POINT_BAR_SIZE)
        self.max_hp = hp
        self.hp = hp

    def update(self, x, y, hp):
        self.rect.x = x
        self.rect.y = y
        self.hp = hp

    def draw(self, surface, camera):
        print(f"{self.rect.x} {self.rect.y}")

        fill = pygame.Surface((self.rect.width, self.rect.height))
        fill.fill((0, 0, 0))
        pygame.draw.rect(fill, (255, 0, 0), (1, 1,
                                                transform_value(self.hp, 0, self.max_hp, 0, self.rect.width - 2),
                                                self.rect.height - 2))

        class operate:
            def __init__(self, fill, x, y):
                self.image = fill.convert()
                self.rect = fill.get_rect()
                self.rect = self.rect.move(x, y)

        operate = operate(fill, self.rect.x, self.rect.y)

        surface.blit(fill, camera.apply(operate))
