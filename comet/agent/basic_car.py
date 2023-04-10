import pygame

import numpy as np

from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from comet import Color, DEBUG

CAR = pygame.image.load("comet/asset/car.png")


class BasicCar:
    accelaration = 0
    stopped = False

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
        self.car_surf = pygame.transform.scale(
            CAR.convert_alpha(), (CAR.get_width() / factor, CAR.get_height() / factor)
        )
        self.width = self.car_surf.get_width()
        self.height = self.car_surf.get_height()

        self.car_center = self.car_surf.get_rect().center

        self.rotated_surf = self.car_surf.copy()
        self.rotated_car_rect = self.rotated_surf.get_rect()

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

        self.angle += self.angular_velocity

    def update(self):
        """Calls rules to determine the value of accelaration and angular_velocity
        and then updates the position of the car
        """
        self.rules()

        if self.stopped:
            self.velocity = 0
            self.accelaration = 0
            self.angular_velocity = 0
            if DEBUG:
                pygame.draw.circle(pygame.display.get_surface(), Color.TICKLE_ME_PINK, (int(self.x), int(self.y)), 50, 2)
            return

        self.angle %= 360

        self.velocity += self.accelaration

        radian = np.radians(self.angle)

        self.x -= np.cos(radian) * self.velocity
        self.y -= np.sin(radian) * self.velocity

        if DEBUG:
            self.trail.append((self.x, self.y, float(self.velocity)))
            if len(self.trail) > 100:
                self.trail.pop(0)

    def draw(self, win: pygame.surface.Surface):
        self.update()

        # +90 is to account for the image being rotated 90 degrees
        self.rotated_surf = pygame.transform.rotate(self.car_surf, angle=-(self.angle) + 90)
        self.rotated_car_rect = self.rotated_surf.get_rect()
        self.car_center = self.rotated_car_rect.center  # half of width and height

        self.rotated_car_rect.move_ip(tuple(np.subtract((self.x, self.y), self.car_center)))

        win.blit(self.rotated_surf, self.rotated_car_rect)

        if DEBUG:
            pygame.draw.circle(win, Color.RED, (self.x, self.y), radius=1)
