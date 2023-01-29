import pygame

import numpy as np

from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from comet import color
from comet.utils import console_stats

CAR = pygame.image.load("comet/asset/car.png")


class BasicCar:
    width = CAR.get_width()
    height = CAR.get_height()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0

        # positve is forward and negative is backward
        self.velocity = 0
        self.rotational_velocity = 0

        # todo: extract to func later
        factor = 10
        self.car_surf = pygame.transform.scale(CAR.convert_alpha(), (self.width / factor, self.height / factor))
        self.car_center = self.car_surf.get_rect().center

        self.rotated_surf = self.car_surf.copy()

    def rules_on_key_press(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_UP]:
            acceleration = 2
            if self.velocity > 15:
                acceleration = 1
            self.velocity = min(100, self.velocity + acceleration)

        if keys_pressed[K_DOWN]:
            if self.velocity > 0:
                self.velocity = max(0, self.velocity - 2)
            else:
                self.velocity = max(-10, self.velocity - 2)

        if keys_pressed[K_LEFT] and int(self.velocity) != 0:
            self.rotational_velocity = min(8, self.rotational_velocity + 1)

        if keys_pressed[K_RIGHT] and self.velocity != 0:
            self.rotational_velocity = max(-8, self.rotational_velocity - 1)

        if not keys_pressed[K_LEFT] and not keys_pressed[K_RIGHT] and self.rotational_velocity != 0:
            self.rotational_velocity *= 0.8

        if not keys_pressed[K_UP] and not keys_pressed[K_DOWN] and self.velocity != 0:
            if self.velocity ** 2 < 0.001:
                self.velocity = 0
            self.velocity *= 0.95

    def update(self):
        self.rules_on_key_press()

        self.angle += self.rotational_velocity

        radian = np.radians(self.angle)

        self.x += np.sin(radian) * self.velocity
        self.y += np.cos(radian) * self.velocity

    def draw(self, win: pygame.surface.Surface):
        self.update()

        self.rotated_surf = pygame.transform.rotate(self.car_surf, angle=self.angle + 180)
        self.car_center = self.rotated_surf.get_rect().center  # half of width and height

        dest = tuple(np.subtract((self.x, self.y), self.car_center))

        win.blit(self.rotated_surf, dest)

        pygame.draw.circle(win, color.WHITE, (self.x, self.y), radius=1)
        console_stats.add(velocity=self.velocity, rotational_velocity=self.rotational_velocity, angle=self.angle)
