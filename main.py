from basicDetails import *
from gamingSpace import wallBlock, foneBlock
from playerModule import Player, Camera, camera_configure, base_player_attack, baseWeapon
from mobs import Boss, base_mob_attack
from menuModule import Game_over


# функция отрисовки группы
def draw_group(group, fill, camera):
    for element in group:
        fill.blit(element.image, camera.apply(element))


# класс игры
class Game:
    def __init__(self, player_sprites):
        pygame.init() # инициализация пайгейма
        self.running = True
        self.end = GAME_IN_PROCESS

        self.clock = pygame.time.Clock()  # создание таймера
        self.window = pygame.display.set_mode(WIN_SIZE) # создание окна

        # группа поражения
        self.game_over = pygame.sprite.Group()
        Game_over.group = self.game_over
        Game_over()

        # группа отвечающая за твердые стены
        self.walls = pygame.sprite.Group()
        wallBlock.group = self.walls

        # группа отвечающая за фоновые блоки
        self.fone = pygame.sprite.Group()
        foneBlock.group = self.fone

        # группа отвечающая за мобов и босса
        self.mobs = pygame.sprite.Group()
        Boss.group = self.mobs

        # группа, отвечающая за атаки мобов и босса
        self.mobs_attack = pygame.sprite.Group()
        base_mob_attack.group = self.mobs_attack

        # группа отвечающая за игрока
        self.group = pygame.sprite.Group()
        Player.group = self.group

        # группа, отвечающая за атаки игрока
        self.players_attack = pygame.sprite.Group()
        base_player_attack.group = self.players_attack

        # группа, отвечающая за оружие
        self.weapons = pygame.sprite.Group()
        baseWeapon.group = self.weapons

        self.camera = Camera(camera_configure, 10000, 1000)     # создание камеры

        # загрузка изображений игрока
        player_spr = os.path.join(PLAYER_SKINS, player_sprites) # создание пути до спрайтов
        Player.move_straight = os.path.join(player_spr, "forward.png")
        Player.move_back = os.path.join(player_spr, "back.png")
        Player.move_left = os.path.join(player_spr, "left.png")
        Player.move_right = os.path.join(player_spr, "right.png")

        self.load_music()   # загрузка музыки
        self.load_level()   # загрузка уровня

    # загрузка музыки
    def load_music(self):
        sounds_player.load(os.path.join(MUSIC_PATH, 'Slipknot Psychosocial.wav'))   # загрузка фоновой музыки
        sounds_player.set_volume(SOUND_LEVEL)   # установка уровня громкости
        sounds_player.play(loops=-1)    # запуск музыки на повторение

    # загрузка уровня
    def load_level(self):
        y = 0

        file_data = open(os.path.join(LEVELS_PATH, '0_level.txt'), mode="r").read().split("\n")     # файл уровня
        texture_path = os.path.join(TEXTURES_PATH, 'Map')   # путь к спрайтам

        # рисование фона и стен
        wallBlock.base_img = os.path.join(texture_path, "BlockWall.png")
        foneBlock.base_img = os.path.join(texture_path, "BlockDown1.png")
        for string in file_data[2:]:
            x = 0
            for symbol in range(len(string)):
                if string[symbol].isdigit():
                    if string[symbol - 1] == WALL_SYMBOL:
                        wallBlock(x, y)
                    elif string[symbol - 1] == FONE_SYMBOL:
                        foneBlock(x, y)
                    x += CELL_SIZE
            y += CELL_SIZE

        self.boss = Boss(*[int(i) for i in file_data[BOSS_INFO].split(",")])    # загрузка босса
        self.player = Player(*[int(i) for i in file_data[PLAYER_SPRITE_INFO].split(",")])   # спаун игрока

    # обработчик событий
    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.running = False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False
                self.player.write_events(events)    # передача событий в обрабочик событий игрока

    # функция обновления
    def update(self):
        if self.end == GAME_IN_PROCESS:
            result = self.player.update(self)   # получение атак игрока
            # если атаки есть, добавляем в группу
            if not result is None:
                self.players_attack.add(result)

            result = self.boss.update(self)     # получение атак мобов
            # если атаки есть, добавляем в группу
            if not result is None:
                self.mobs_attack.add(result)

            # обновление групп
            self.players_attack.update(self)    # обновление атак игрока
            self.mobs_attack.update(self)   # обновление атак босса
            self.walls.update(self)     # обновление стен

            # проверка: жив, ли игрок
            if self.player.is_dead():
                self.end = GAME_OVER

            # проверка: жив, ли босс
            if self.boss.is_dead():
                self.end = WIN

        elif self.end == GAME_OVER:
            self.game_over.update()

        self.clock.tick(FPS)  # поддержка частоты кадров

    def render(self):
        if self.end == GAME_IN_PROCESS:
            self.window.fill((0, 0, 100))   # закраска холста

            self.camera.update(self.player)     # обновление камеры

            # отрисовка стен и фона
            draw_group(self.walls, self.window, self.camera)
            draw_group(self.fone, self.window, self.camera)

            self.player.draw(self.window, self.camera)  # рисование игрока
            self.boss.draw(self.window, self.camera)    # рисование моба

            # отрисовка груп атак
            draw_group(self.players_attack, self.window, self.camera)
            draw_group(self.mobs_attack, self.window, self.camera)

        elif self.end == GAME_OVER:
            self.window.fill((0, 0, 0))
            self.camera.update(self.player)
            for e in self.game_over:
                self.window.blit(e.image, self.camera.apply(e))

        pygame.display.flip()   # обновление экрана

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()
        pygame.quit()


if __name__ == '__main__':
    Game().run()