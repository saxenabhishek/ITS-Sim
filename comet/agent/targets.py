import numpy as np
import pygame

from comet.utils import stats
from comet import Color


class Path:
    step = 0

    def __init__(self, *coordinates):
        coordinates = np.concatenate(coordinates)
        self.x = coordinates[0][0]
        self.y = coordinates[0][1]
        self.coordinates = coordinates

    def next(self):
        if self.hasNext():
            self.step += 1
            self.x, self.y = self.coordinates[self.step]
            return True
        return False

    def hasNext(self):
        return self.step + 1 < len(self.coordinates) - 1

    def draw(self, screen):
        pygame.draw.lines(screen, Color.TICKLE_ME_PINK, False, self.coordinates, 5)

    def reset(self):
        self.step = -1
        self.next()


def straight_road(origin, length, angle):
    step = 10
    line = np.arange(2, step * length, step, dtype=np.int32)
    x = (line * np.cos(np.radians(angle))) + origin[0]
    y = (line * np.sin(np.radians(angle))) + origin[1]
    return np.array([x, y]).T
