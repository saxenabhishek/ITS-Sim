from comet.agent.follow_car import FollowCar
from comet import SCALE
from comet.targets import Tracker
import numpy as np
import random


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
        # self.next_car_tracker = Tracker(-1, -1)
        self.collision_adjustment = 0
        self.MAX_VELOCITY, self.MAX_ACCELERATION = random.choice([(3, 0.05), (8, 0.08)])

    def rules(self):
        desired_angle = self._angle_to_target()


        # diff_in_angle = ((desired_angle % 360) - self.angle) % 360

        # self.angular_velocity = min(diff_in_angle * 0.5, 50)

        # if diff_in_angle < 190:
        #     self.angle += self.angular_velocity
        # elif diff_in_angle > 170:
        #     self.angle -= self.angular_velocity

        # Instead  of adjusting angular velocity, we adjust the angle directly
        self.angle = desired_angle

        self.acceleration = self.MAX_ACCELERATION * (1 - np.power((self.velocity / self.MAX_VELOCITY), 4))

        self.acceleration = self.acceleration + self.collision_adjustment

        self.collision_adjustment = 0

        if self.acceleration < 0 and self.stopped is -1:
            self.acceleration = 0
            self.velocity = 0

        self._update_target_tracker()

    def collides_with(self, other_car_x: float, other_car_y: float, other_car_velocity: float):
        s0 = 25  # minimum distance
        T = 1.5  # time gap
        b = 3


        s = self._euclidean_distance_to_(other_car_x, other_car_y) - self.width
        velocity_difference = self.velocity - other_car_velocity

        if abs(velocity_difference) > 10:
            self.collision_adjustment -= np.power(self.velocity * velocity_difference, 2) / 4 * b * np.power(s, 2)
        else:
            self.collision_adjustment -= self.MAX_ACCELERATION * np.power((s0 + self.velocity * T), 2) / np.power(s, 2)
