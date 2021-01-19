from basicDetails import *


HElTH_POINT_BAR_SIZE = 10


# преобразование значения из одного диапозона в другой
def transform_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# класс полоски жизни
class helthPointBar():
    def __init__(self, size, hp):
        self.rect = pygame.Rect(0, 0, size, HElTH_POINT_BAR_SIZE)
        self.max_hp = hp    # максимальный уровень hp
        self.hp = hp    # hp на данный момент

    # обновление позиции прямоугольника и уровня hp
    def update(self, x, y, hp):
        self.rect.x = x
        self.rect.y = y
        self.hp = hp

    # отрисовка линии жизни
    def draw(self, surface, camera):
        fill = pygame.Surface((self.rect.width, self.rect.height))  # создание холста для рисования
        fill.fill((0, 0, 0))    # заливка поля черным
        pygame.draw.rect(fill, (255, 0, 0), (1, 1,
                                             transform_value(self.hp, 0, self.max_hp, 0, self.rect.width - 2),
                                             self.rect.height - 2))  # рисование прямоугольника жизни

        # класс заглушка, необходим для корректоной обработки прямоугольника камерой
        class Operate:
            def __init__(self, fill, x, y):
                self.image = fill.convert()     # преобразование холста в изображение
                self.rect = fill.get_rect()     # получение прямоугольника изображения
                self.rect = self.rect.move(x, y)    # перемещение прямоугольника

        operate = Operate(fill, self.rect.x, self.rect.y)

        surface.blit(fill, camera.apply(operate))   # отрисовка линейки жизни
