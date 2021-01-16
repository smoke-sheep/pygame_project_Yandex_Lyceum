from basicDetails import *
from gamingSpace import wallBlock, baseBlock, foneBlock
from playerModule import Object, Camera, camera_configure, base_player_attack, baseWeapon
from mobs import Boss, base_mob_attack
from menuModule import Game_over


"""
def window_init():
    # получаем размеры монитора
    # в pygame неудобно получать размер монитора, поэтому воспользуемся
    # другой библиотекой
    from tkinter import Tk
    from os import environ
    temp = Tk()
    MONITOR_SIZE = temp.winfo_screenwidth(), temp.winfo_screenheight()
    temp.destroy()
    del temp

    # помещаем окно в верхний правый угол экрана
    # это нужно сделать до того, как вы создадите окно
    #screen_coords = (MONITOR_SIZE[0] - WIN_SIZE.w - 50, 50)
    #environ['SDL_VIDEO_WINDOW_POS'] = f"{screen_coords[0]}, {screen_coords[1]}"

    screen = pygame.display.set_mode(MONITOR_SIZE)

    return screen
"""


class Game:
    def __init__(self, player_sprites):
        pygame.init()
        self.running = True
        self.end = GAME_IN_PROCESS

        self.clock = pygame.time.Clock()  # создание таймера
        self.window = pygame.display.set_mode(WIN_SIZE) #window_init() #pygame.display.set_mode(WIN_SIZE)

        self.game_over = pygame.sprite.Group()
        Game_over.group = self.game_over
        Game_over()

        self.walls = pygame.sprite.Group()
        wallBlock.group = self.walls

        self.fone = pygame.sprite.Group()
        baseBlock.group = self.fone
        foneBlock.group = self.fone

        self.mobs = pygame.sprite.Group()
        Boss.group = self.mobs

        self.mobs_attack = pygame.sprite.Group()
        base_mob_attack.group = self.mobs_attack

        self.players_attack = pygame.sprite.Group()
        base_player_attack.group = self.players_attack

        self.weapons = pygame.sprite.Group()
        baseWeapon.group = self.weapons

        self.camera = Camera(camera_configure, 10000, 1000)

        player_spr = os.path.join(PLAYER_SKINS, player_sprites)
        Object.move_straight = os.path.join(player_spr, "forward.png")
        Object.move_back = os.path.join(player_spr, "back.png")
        Object.move_left = os.path.join(player_spr, "left.png")
        Object.move_right = os.path.join(player_spr, "right.png")

        self.load_music()
        self.load_level()

    def load_music(self):
        sounds_player.load(os.path.join(MUSIC_PATH, 'Slipknot Psychosocial.wav'))
        sounds_player.set_volume(SOUND_LEVEL)
        sounds_player.play(loops=-1)

    def load_level(self):
        y = 0

        file_data = open(os.path.join(LEVELS_PATH, '0_level.txt'), mode="r").read().split("\n")
        texture_path = os.path.join(TEXTURES_PATH, 'Map')

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

        self.boss = Boss(*[int(i) for i in file_data[BOSS_INFO].split(",")])

        self.group = pygame.sprite.Group()
        Object.group = self.group
        self.player = Object(*[int(i) for i in file_data[PLAYER_SPRITE_INFO].split(",")])

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                self.running = False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False
                self.player.write_events(events)

    def update(self):
        if self.end == GAME_IN_PROCESS:
            result = self.player.update(self)
            if not result is None:
                #print(result)
                self.players_attack.add(result)

            result = self.boss.update(self)
            if not result is None:
                self.mobs_attack.add(result)

            self.players_attack.update(self)
            self.mobs_attack.update(self)
            self.walls.update(self)

            if self.player.is_dead():
                self.end = GAME_OVER
                #self.running = False

            if self.boss.is_dead():
                self.end = WIN
                #self.running = False

        elif self.end == GAME_OVER:
            self.game_over.update()

        self.clock.tick(FPS)  # поддержка частоты кадров

    def render(self):
        if self.end == GAME_IN_PROCESS:
            self.window.fill((0, 0, 100))

            #self.walls.draw(self.window)
            #self.fone.draw(self.window)

            self.camera.update(self.player)

            for e in self.walls:
                self.window.blit(e.image, self.camera.apply(e))
            for e in self.fone:
                self.window.blit(e.image, self.camera.apply(e))

            for e in self.group:
                e.draw(self.window, self.camera.apply(e))

            for e in self.mobs:
                e.draw(self.window, self.camera.apply(e))

            for e in self.players_attack:
                self.window.blit(e.image, self.camera.apply(e))

            for e in self.mobs_attack:
                self.window.blit(e.image, self.camera.apply(e))

        elif self.end == GAME_OVER:
            self.window.fill((0, 0, 0))
            # self.game_over.draw(self.window)
            self.camera.update(self.player)
            for e in self.game_over:
                self.window.blit(e.image, self.camera.apply(e))
            #self.window.blit(self.game_over.image, self.game_over.rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()
        pygame.quit()


if __name__ == '__main__':
    Game().run()