import numpy as np
import pygame
from comet import Color, SCALE, DEBUG


class Tracker:
    def __init__(self, x_target: int, y_target: int) -> None:
        """
        Data store, personal to each CAR, will track anything that needs to be recorded
        An extension of the Basic car itself under a sub class
        :param x: x coordinate of the car
        :type x: int
        :param y: y coordinate of the car
        :type y: int
        """
        self.x = x_target
        self.y = y_target
        self.ended = False
        self.step = 0
        self.end_time = -1
        self.distance = 0.0
        self.start_time = 0.1
        self.run_time = 0.0
        self.avg_speed = 0.0


class Path:
    def __init__(self, *args):
        """
        Path is a collection of coordinates that any number of cars will follow
        keeps track of the navigation of the cars and updates their Trackers as required
        """
        coordinates = np.concatenate(args)
        self.origin_x = coordinates[0][0]  # x coordinate of the first point
        self.origin_y = coordinates[0][1]  # y coordinate of the first point
        self.start = (self.origin_x, self.origin_y)
        self.coordinates = coordinates

        self.total_distance = 0  # in pixels
        for i in range(1, len(coordinates)):
            self.total_distance += np.sqrt(np.sum(np.subtract(coordinates[i], coordinates[i - 1]) ** 2, axis=0))

    def hasNext(self, step):
        return step < len(self.coordinates)

    def update(self, target: Tracker):
        target.x, target.y = self.coordinates[target.step]
        target.step += 1

    def end_run(self, target: Tracker):
        target.end_time = pygame.time.get_ticks()
        target.ended = True
        run_time = (target.end_time - target.start_time) / 1000  # in seconds
        target.run_time = run_time * 20  # increase game time by 20%
        target.avg_speed = self.total_distance / run_time * 3.6  # in km/h

    def draw(self, screen):
        pygame.draw.lines(screen, Color.CULTURED, False, self.coordinates, 3)
        if DEBUG:
            colors = [Color.AMBER, Color.TICKLE_ME_PINK, Color.CYAN]
            i = 0
            while i < len(self.coordinates):
                pygame.draw.circle(screen, colors[i % len(colors)], self.coordinates[i], 3)
                i += 1


def straight_road(origin, length, angle):
    step = 20
    line = np.arange(1, step * length, step, dtype=np.int32) + step
    x = (line * np.cos(np.radians(angle))) + origin[0]
    y = (line * np.sin(np.radians(angle))) + origin[1]
    return np.array([x, y]).T
