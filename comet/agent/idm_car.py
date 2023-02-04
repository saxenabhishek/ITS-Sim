import numpy as np
import pygame

from comet.agent.follow_car import FollowCar
from comet import DEBUG


class IDMCar(FollowCar):
    def __init__(self, x, y, target):
        """
        Car that implements the Intelligent Driver Model

        :param x: x coordinate
        :param y: y coordinate
        :param target: target to follow

        Must be a class with x and y attributes
        """
        super().__init__(x, y, target)

    def rules(self):
        desired_angle = self._angle_to_target()

        self.angle = desired_angle

        self.accelaration = self.MAX_ACCELERATION * (1 - (self.velocity / 5) ** 4)

        self._update_target_tracker()
