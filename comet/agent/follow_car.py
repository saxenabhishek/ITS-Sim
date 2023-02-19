import numpy as np
import pygame

from comet.agent.basic_car import BasicCar
from comet import DEBUG, Color
from comet.targets import Tracker, Path


class FollowCar(BasicCar):
    MAX_ACCELERATION = 0.05
    MAX_VELOCITY = 5.0

    def __init__(self, x: int, y: int, path: Path):
        """
        Car that follows a target with constat velocity and constatn angular acceleration
        :param x: x coordinate
        :param y: y coordinate
        :param target: target to follow

        Must be a class with x and y attributes
        """
        super().__init__(x, y)
        self.path = path
        self.tracker = Tracker(path.origin_x, path.origin_y)

    def rules(self):
        desired_angle = self._angle_to_target()

        self.accelaration = self.MAX_ACCELERATION * (1 - (self.velocity / self.MAX_VELOCITY) ** 4)

        angular_acceleration = 0.1 * (1 - (self.angular_velocity / 10) ** 4)
        self.angular_velocity += angular_acceleration

        # anything near 180 should be treated as 180
        if ((desired_angle % 360) - self.angle) % 360 < 180:
            self.angle += self.angular_velocity
        else:
            self.angle -= self.angular_velocity

        self._update_target_tracker()

    def _update_target_tracker(self):
        """
        Check if we are close to the current tracker and if so, update the tracker
        to the next one in the path. If there are no more trackers, stop the car and end the episode
        """
        if self._distance_to_target() < self.width:
            if not self.path.update(self.tracker):
                self.stopped = True
            if not self.path.hasNext(self.tracker.step):
                self.path.end_run(self.tracker)
                self.stopped = True

    def _distance_to_target(self):
        return self._euclidean_distance_to_(self.tracker.target_x, self.tracker.target_y)

    def _euclidean_distance_to_(self, x, y):
        subtracted_points = np.subtract((self.x, self.y), (x, y))
        power = np.power(subtracted_points, 2)
        return np.sqrt(np.sum(power, axis=0))

    def _angle_to_target(self):
        return 57.2958 * np.arctan2(self.y - self.tracker.target_y, self.x - self.tracker.target_x)

    def update(self):
        super().update()
        self.tracker.distance += self.velocity
        self.tracker.x = self.x
        self.tracker.y = self.y
        self.tracker.velocity = self.velocity

    def draw(self, win: pygame.surface.Surface):
        if DEBUG:
            pygame.draw.circle(win, Color.CULTURED, (self.tracker.target_x, self.tracker.target_y), radius=10)
            base_point = (
                min(self.x, self.tracker.target_x)
                if self.x < self.tracker.target_x
                else max(self.tracker.target_x, self.x),
                min(self.y, self.tracker.target_y)
                if self.y > self.tracker.target_y
                else max(self.tracker.target_y, self.y),
            )
            pygame.draw.line(win, (200, 100, 100), (self.x, self.y), (self.tracker.target_x, self.tracker.target_y))
            pygame.draw.circle(win, (200, 100, 100), base_point, 10)
        return super().draw(win)

    def reset(self):
        # assuming target reset is called first
        self.tracker = Tracker(self.path.origin_x, self.path.origin_y)
        self.x = self.tracker.target_x
        self.y = self.tracker.target_y

        self.velocity = 0
        self.angle = 0
        self.angular_velocity = 0
        self.stopped = False
