import numpy as np
import pygame
from comet import Color


class Tracker:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.step = 0


class Path:
    def __init__(self, *args):
        coordinates = np.concatenate(args)
        self.origin_x = coordinates[0][0]  # x coordinate of the first point
        self.origin_y = coordinates[0][1]  # y coordinate of the first point
        self.coordinates = coordinates

    def hasNext(self, step):
        return step + 1 < len(self.coordinates) - 1

    def update(self, target):
        target.x, target.y = self.coordinates[target.step]
        target.step += 1

    def draw(self, screen):
        pygame.draw.lines(screen, Color.TICKLE_ME_PINK, False, self.coordinates, 5)


def straight_road(origin, length, angle):
    step = 10
    line = np.arange(2, step * length, step, dtype=np.int32)
    x = (line * np.cos(np.radians(angle))) + origin[0]
    y = (line * np.sin(np.radians(angle))) + origin[1]
    return np.array([x, y]).T
