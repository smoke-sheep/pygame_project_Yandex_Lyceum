import pygame as pg
from pygame.locals import *
import os

from basicDetails import *
from playerElements.CameraModule import camera_configure, Camera
from playerElements.Atacks import base_player_attack
from playerElements.weapoints import baseWeapon, blackGun, wizardRoad
from informBarModule import helthPointBar


class Object(pg.sprite.Sprite):
    group = None
    img = os.path.join(TEXTURES_PATH, 'creature.png')

    move_straight = None
    move_left = None
    move_right = None
    move_back = None

    def __init__(self, x, y):
        super().__init__(Object.group)
        self.image = load_image(Object.img, -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.speed = 10
        self.health_point = 500

        self.events = None

        self.weapoint_pos = (10, 10)
        x = self.rect.x + self.weapoint_pos[0]
        y = self.rect.y + self.weapoint_pos[1]
        print(x, y)
        self.weapons = [blackGun(x, y), wizardRoad(x, y)]
        self.active_weapon = 0

        self.health_point_bar = helthPointBar(self.rect.width, self.health_point)
        # Object.group.add(self)
        # self.add(Object.group)

    def write_events(self, events):
        self.events = events

    def processing_events(self):
        out_data = None
        if not self.events is None:
            for event in self.events:
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        out_data = self.weapons[self.active_weapon].attack()
                    elif event.key == K_f:
                        self.active_weapon -= 1
                        if self.active_weapon < 0:
                            self.active_weapon = len(self.weapons) - 1
                    elif event.key == K_g:
                        self.active_weapon += 1
                        if self.active_weapon >= len(self.weapons):
                            self.active_weapon = 0

            self.events = None
        return out_data

    def update(self, data):
        keys = pg.key.get_pressed()
        left = keys[K_a] or keys[K_LEFT]
        right = keys[K_d] or keys[K_RIGHT]
        up = keys[K_w] or keys[K_UP]
        down = keys[K_s] or keys[K_DOWN]

        if left == right:
            speed_x = 0
        elif left:
            speed_x = -self.speed
        else:
            speed_x = self.speed
        self.rect.x += speed_x

        if up == down:
            speed_y = 0
        elif up:
            speed_y = -self.speed
        else:
            speed_y = self.speed
        self.rect.y += speed_y

        if pg.sprite.spritecollide(self, data.walls, False) or pg.sprite.spritecollide(self, data.mobs, False):
            #print("YES")
            self.rect.x -= speed_x
            self.rect.y -= speed_y

        damage = pg.sprite.spritecollide(self, data.mobs_attack, True)
        if bool(damage):
            for attack in damage:
                self.health_point -= attack.get_damage()
                print(f"hp: {self.health_point}")

        x = self.rect.x + self.weapoint_pos[0]
        y = self.rect.y + self.weapoint_pos[1]
        self.weapons[self.active_weapon].update(x, y)

        if not self.is_dead():
            print(f"{self.rect.x} {self.rect.y}")
            self.health_point_bar.update(self.rect.x, self.rect.y, self.health_point)

        return self.processing_events()

    def draw(self, fill, camera):
        fill.blit(self.image, camera)
        self.weapons[self.active_weapon].draw(fill, camera)
        self.health_point_bar.draw(fill, camera)

    def is_dead(self):
        if self.health_point <= 0:
            return True
        return False

    """def draw_bars(self, surface):
        self.health_point_bar.draw(surface)"""
