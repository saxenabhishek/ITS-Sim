"""
Environment to create paths and to report back
"""
import pygame
from comet.targets import Path, Tracker
from comet.agent import IDMCar
from comet.utils import stats
import pandas as pd
from typing import List


class City:
    time_rn = pygame.time.get_ticks()
    INSERTION_TIME = 1000
    INSERT_EVENT = pygame.USEREVENT + 1

    def __init__(self) -> None:
        """
        Create paths, creat cars, give cars next instruction

        """
        self.paths: List[Path] = []
        self.cars: List[IDMCar] = []
        self.trackers: List[Tracker] = []
        self.time = 0
        pygame.time.set_timer(City.INSERT_EVENT, City.INSERTION_TIME)

    def add_path(self, road: Path):
        self.paths.append(road)
        newcar = IDMCar(*road.start, road)
        newcar.target.start_time = pygame.time.get_ticks()
        self.cars.append(newcar)

    def consume_car_event(self):
        for path in self.paths:
            newcar = IDMCar(*path.start, path)
            newcar.target.start_time = pygame.time.get_ticks()
            self.cars.append(newcar)

    def draw_agents(self, win):
        for path in self.paths:
            path.draw(win)

        for car in self.cars:
            if car.target.ended:
                self.trackers.append(car.target)
                self.cars.remove(car)

            car.draw(win)

        stats.add(cars=len(self.cars), paths=len(self.paths), Tracker=len(self.trackers))

    def process_trackers(self):
        """add them to CSV file"""
        df = pd.DataFrame([tracker.__dict__ for tracker in self.trackers])
        print(df)
        self.trackers.clear()

    def reset(self):
        for car in self.cars:
            car.reset()
