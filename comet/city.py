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
    total_cars = 0

    def __init__(self) -> None:
        """
        Create paths, creat cars, give cars next instruction

        """

        self.roads: List[dict] = []
        self.trackers: List[Tracker] = []
        self.time = 0
        pygame.time.set_timer(City.INSERT_EVENT, City.INSERTION_TIME)

    def add_path(self, road: Path):
        self.total_cars = 1
        newcar = IDMCar(*road.start, road)
        newcar.tracker.start_time = pygame.time.get_ticks()
        self.roads.append({"road": road, "cars": [newcar]})

    def consume_car_event(self):
        for road in self.roads:
            self.total_cars += 1
            path: Path = road["road"]
            newcar = IDMCar(*path.start, path)
            newcar.tracker.start_time = pygame.time.get_ticks()
            road["cars"].append(newcar)

    def draw_agents(self, win):
        for road in self.roads:
            road["road"].draw(win)
            for car in road["cars"]:
                if car.tracker.ended:
                    self.trackers.append(car.tracker)
                    road["cars"].remove(car)
                car.draw(win)

        stats.add(cars=self.total_cars, paths=len(self.roads), Tracker=len(self.trackers))

    def process_trackers(self):
        """add them to CSV file"""
        df = pd.DataFrame([tracker.__dict__ for tracker in self.trackers])
        print(df)
        self.trackers.clear()

    def reset(self):
        for car in self.cars:
            car.reset()
