"""
Environment to create paths and to report back
"""
import pygame
from comet import Color
from comet.targets import Path, Tracker
from comet.agent import IDMCar
from comet.utils import stats
import pandas as pd
from typing import List
import numpy as np


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
            if car.tracker.ended:
                car.tracker.__dict__.update(car.__dict__)
                self.trackers.append(car.tracker)

                self.cars.remove(car)

            line = np.arange(car.height / 2 - 1, 200, car.height / 2, dtype=np.int32)
            x, y = (
                line * np.cos(np.radians(car.angle + 180)) + car.x,
                line * np.sin(np.radians(car.angle + 180)) + car.y,
            )

            car.next_car_tracker = Tracker(-1, -1)
            # TODO: make this more readable
            for point in np.array([x, y]).T:
                # pygame.draw.circle(win, Color.BLACK, point, 3)
                flag = 0
                for other_car in self.cars:
                    if car != other_car and other_car.rotated_car_rect.collidepoint(point):
                        car.next_car_tracker = other_car.tracker
                        flag = 1
                        break
                if flag:
                    break
            car.draw(win)

        stats.add(cars=len(self.cars), paths=len(self.paths), Tracker=len(self.trackers))

    def process_trackers(self):
        """add them to CSV file"""

        df = pd.DataFrame([tracker.__dict__ for tracker in self.trackers])
        df.drop(columns=["path", "next_car_tracker", "ended", "target_x", "target_y", "tracker"], inplace=True)
        print(df.columns)

        self.trackers.clear()

    def reset(self):
        for car in self.cars:
            car.reset()
