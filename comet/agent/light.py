import pygame
from comet import Color, DEBUG
import numpy as np
from comet.agent import IDMCar
from typing import List


class Light:
    def __init__(self, location: np.ndarray):
        self.loc = location
        self.touched = False
        self.color: tuple = Color.RED

    def check_touched(self, cars: List[IDMCar]):
        for car in cars:
            if car.rotated_car_rect.collidepoint(tuple(self.loc)):
                self.touched = True  # dead code
                if self.color == Color.RED:
                    car.stopped = pygame.time.get_ticks()

    def draw(self, win: pygame.surface.Surface):
        if self.touched:
            pygame.draw.circle(win, Color.AMBER, tuple(self.loc), 8)
        pygame.draw.circle(win, self.color, tuple(self.loc), 5)
        self.touched = False
