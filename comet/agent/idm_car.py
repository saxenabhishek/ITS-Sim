from comet.agent.follow_car import FollowCar
from comet import SCALE
from comet.targets import Tracker
import numpy as np
import random


class IDMCar(FollowCar):
    flag = 0

    def __init__(self, x, y, target):
        """
        Car that implements the Intelligent Driver Model

        :param x: x coordinate
        :param y: y coordinate
        :param target: target to follow

        Must be a class with x and y attributes
        """
        super().__init__(x, y, target)
        self.next_car_tracker = Tracker(-1, -1)
        self.MAX_VELOCITY = random.uniform(3, 8)
        self.MAX_ACCELERATION = random.uniform(0.5, 1.5)

    def rules(self):
        s0 = 50  # minimum distance
        T = 1.5  # time gap
        b = 3

        desired_angle = self._angle_to_target()

        # Instead  of adjusting angular velocity, we adjust the angle directly
        self.angle = desired_angle

        self.accelaration = self.MAX_ACCELERATION * (1 - np.power((self.velocity / self.MAX_VELOCITY), 4))

        if self.next_car_tracker.x != -1:
            s = self._euclidean_distance_to_(self.next_car_tracker.x, self.next_car_tracker.y) - self.width
            velocity_difference = self.velocity - self.next_car_tracker.velocity

            if abs(velocity_difference) > 5:
                self.flag = 1
                self.accelaration -= np.power(self.velocity * velocity_difference, 2) / 4 * b * np.power(s, 2)
            else:
                self.flag = 0
                self.accelaration -= self.MAX_ACCELERATION * np.power((s0 + self.velocity * T), 2) / np.power(s, 2)

        if self.accelaration > 0:
            self.stopped = False
        else:
            self.accelaration = 0
            self.velocity = 0
            self.stopped = True

        self._update_target_tracker()
