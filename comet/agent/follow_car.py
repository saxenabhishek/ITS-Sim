import numpy as np
import pygame

from comet.agent.basic_car import BasicCar
from comet.utils import stats
from comet import DEBUG


class FollowCar(BasicCar):
    MAX_ACCELERATION = 0.05

    def __init__(self, x, y, target):
        """
        Car that follows a target with constat velocity and constatn angular acceleration
        :param x: x coordinate
        :param y: y coordinate
        :param target: target to follow

        Must be a class with x and y attributes
        """
        super().__init__(x, y)
        self.target = target

    def rules(self):
        distance = np.sqrt(np.sum(np.subtract((self.x, self.y), (self.target.x, self.target.y)) ** 2, axis=0))
        desired_angle = 57.2958 * np.arctan2(self.y - self.target.y, self.x - self.target.x)

        self.accelaration = self.MAX_ACCELERATION * (1 - (self.velocity / 5) ** 4)

        angular_acceleration = 0.1 * (1 - (self.angular_velocity / 10) ** 4)
        self.angular_velocity += angular_acceleration

        # anything near 180 should be treated as 180
        if ((desired_angle % 360) - self.angle) % 360 < 180:
            self.angle += self.angular_velocity
        else:
            self.angle -= self.angular_velocity

        if distance < 30 and not self.target.next():
            self.stopped = True

    def draw(self, win: pygame.surface.Surface):
        if DEBUG:
            base_point = (
                min(self.x, self.target.x) if self.x < self.target.x else max(self.target.x, self.x),
                min(self.y, self.target.y) if self.y > self.target.y else max(self.target.y, self.y),
            )
            pygame.draw.line(win, (200, 100, 100), (self.x, self.y), (self.target.x, self.target.y))
            pygame.draw.circle(win, (200, 100, 100), base_point, 10)
        return super().draw(win)

    def reset(self):
        # assuming target reset is called first
        self.x = self.target.x
        self.y = self.target.y
        self.velocity = 0
        self.angle = 0
        self.angular_velocity = 0
        self.stopped = False
