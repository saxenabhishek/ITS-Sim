import pygame

import numpy as np

from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from comet import color, DEBUG
from comet.utils import stats

CAR = pygame.image.load("comet/asset/car.png")


class BasicCar:
    width = CAR.get_width()
    height = CAR.get_height()

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.angle = 0

        # positve is forward and negative is backward
        self.velocity = 0
        self.angular_velocity = 0

        self.trail = [(x, y, 1.0)]

        # todo: extract to func later
        factor = 15
        self.car_surf = pygame.transform.scale(CAR.convert_alpha(), (self.width / factor, self.height / factor))
        self.car_center = self.car_surf.get_rect().center

        self.rotated_surf = self.car_surf.copy()

    def rules(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_UP]:
            acceleration = 2
            if self.velocity > 15:
                acceleration = 1
            self.velocity = min(50, self.velocity + acceleration)

        if keys_pressed[K_DOWN]:
            if self.velocity > 0:
                self.velocity = max(0, self.velocity - 2)
            else:
                self.velocity = max(-10, self.velocity - 2)

        if keys_pressed[K_RIGHT] and int(self.velocity) != 0:
            self.angular_velocity = min(8, self.angular_velocity + 1)

        if keys_pressed[K_LEFT] and self.velocity != 0:
            self.angular_velocity = max(-8, self.angular_velocity - 1)

        if not keys_pressed[K_LEFT] and not keys_pressed[K_RIGHT] and self.angular_velocity != 0:
            self.angular_velocity *= 0.8

        if not keys_pressed[K_UP] and not keys_pressed[K_DOWN] and self.velocity != 0:
            if self.velocity**2 < 0.01:
                self.velocity = 0
            self.velocity *= 0.95

    def update(self):
        self.rules()

        self.trail.append((self.x, self.y, self.velocity))
        if len(self.trail) > 100:
            self.trail.pop(0)

        self.angle += self.angular_velocity

        self.angle %= 360

        radian = np.radians(self.angle)

        self.x -= np.cos(radian) * self.velocity
        self.y -= np.sin(radian) * self.velocity

        stats.add(velocity=self.velocity, angular_velocity=self.angular_velocity, angle=self.angle)

    def draw(self, win: pygame.surface.Surface):
        self.update()

        # +90 is to account for the image being rotated 90 degrees
        self.rotated_surf = pygame.transform.rotate(self.car_surf, angle=-(self.angle) + 90)
        self.car_center = self.rotated_surf.get_rect().center  # half of width and height

        dest = tuple(np.subtract((self.x, self.y), self.car_center))

        win.blit(self.rotated_surf, dest)

        if DEBUG:
            for i, point in enumerate(self.trail):
                pygame.draw.circle(win, Color.CULTURED, point[:-1], radius=min(30, point[-1] / 2))
            pygame.draw.circle(win, Color.RED, (self.x, self.y), radius=1)
