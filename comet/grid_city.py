import random
from comet import SCREEN_HEIGHT, SCREEN_WIDTH, Color, default_font
from comet.utils import stats
import numpy as np
import pygame
from comet.targets import Path
from comet.agent import IDMCar, Light, Junction
from typing import List
import pandas as pd
import time
from statistics import mean


class GridCity:
    GRID_SIZE = 90
    LANE_WIDTH = 20
    INSERTION_TIME = 1000
    INSERT_EVENT = pygame.USEREVENT + 1
    SHIFT_TIME = 3000
    SHIFT_EVENT = pygame.USEREVENT + 2

    def __init__(self):
        self.init_graph()
        self.init_lights()
        self.init_paths(20)

        pygame.time.set_timer(self.INSERT_EVENT, self.INSERTION_TIME, loops=0)
        pygame.time.set_timer(self.SHIFT_EVENT, self.SHIFT_TIME, loops=0)

    def init_graph(self):
        self.graph = {}
        for x in range(SCREEN_WIDTH // self.GRID_SIZE):
            for y in range(SCREEN_HEIGHT // self.GRID_SIZE):
                vertex = (x, y)
                neighbors = []
                if x > 0:
                    neighbors.append((x - 1, y))
                if x < SCREEN_WIDTH // self.GRID_SIZE - 1:
                    neighbors.append((x + 1, y))
                if y > 0:
                    neighbors.append((x, y - 1))
                if y < SCREEN_HEIGHT // self.GRID_SIZE - 1:
                    neighbors.append((x, y + 1))
                neighbors = random.choices(neighbors, k=random.randint(0, len(neighbors)))
                self.graph[vertex] = list(set(self.graph.get(vertex, []) + neighbors))

                for neighbor in neighbors:
                    if neighbor not in self.graph:
                        self.graph[neighbor] = [vertex]
                    if vertex not in self.graph[neighbor]:
                        self.graph[neighbor].append(vertex)

    def init_paths(self, N, steps=5):
        """
        Initialize N random paths in the grid city based on the given graph structure.
        """
        self.cars: List[IDMCar] = []
        paths = []
        for i in range(N):
            # 1. Select a random vertex and a random number of steps
            vertex = random.choice(list(self.graph.keys()))
            num_steps = random.randint(4, steps)

            # Initialize path array and add the starting point
            path = []

            vertex = np.array(vertex)

            visited = {tuple(vertex)}
            for j in range(num_steps):
                # 2. Select a connected vertex and calculate the pixel value of the point that is perpendicular and
                # shifted by half the value of lane width, update the new vertex.

                options = list(filter(lambda x: x not in visited, self.graph[tuple(vertex)]))

                if len(options) == 0:
                    break

                neighbor = random.choice(options)
                neighbor = np.array(neighbor)

                edge_vector = neighbor - vertex

                perpendicular_vector = np.array([-edge_vector[1], edge_vector[0]]) / self.GRID_SIZE
                shift = perpendicular_vector * self.LANE_WIDTH / 2

                # new_vertex = np.add(np.multiply(np.add(vertex, neighbor), 0.5), shift)

                new_vertex = vertex + shift
                # new_vertex = np.round(new_vertex).astype(int)

                # Add the new vertex to the path
                path.append(tuple(new_vertex))
                visited.add(tuple(neighbor))
                vertex = neighbor

            path.append(tuple(vertex + shift))

            # 3. Make an array of pixel values
            path = self.convert_grid_loc_to_pixel(path)
            # path = path.round().astype(int)

            # 4. Append the new path to the list of paths
            if path.shape[0] > 2:
                paths.append(Path(path))

        self.paths: List[Path] = paths

    def init_lights(self):
        self.junctions: List[Junction] = []

        for vertex, neighbors in self.graph.items():
            if len(neighbors) < 3:
                continue

            vertex = np.array(vertex)
            junction_lights = []

            for neighbor in neighbors:
                neighbor = np.array(neighbor)
                edge_vector = neighbor - vertex

                perpendicular_vector = np.array([-edge_vector[1], edge_vector[0]]) / self.GRID_SIZE
                shift = perpendicular_vector * self.LANE_WIDTH

                new_vertex = vertex - shift

                vertex_pixel = self.convert_grid_loc_to_pixel(new_vertex)
                neighbor_pixel = self.convert_grid_loc_to_pixel(neighbor)

                coordinates = np.linspace(vertex_pixel, neighbor_pixel, 4).astype(int)
                junction_lights.append(Light(coordinates[1]))

            self.junctions.append(Junction(junction_lights))

    def process_event(self, event):
        if event.type == self.INSERT_EVENT:
            self.add_car_to_city()
        if event.type == self.SHIFT_EVENT:
            for junction in self.junctions:
                junction.shift_light()
            for car in self.cars:
                car.stopped = -1

    def add_car_to_city(self):
        path = random.choice(self.paths)
        if any([car.rotated_car_rect.collidepoint(path.start) for car in self.cars]):
            return
        newcar = IDMCar(*path.start, path)
        newcar.tracker.start_time = pygame.time.get_ticks()
        self.cars.append(newcar)

    def convert_grid_loc_to_pixel(self, pos):
        return np.array(pos) * self.GRID_SIZE + self.GRID_SIZE // 2

    # dead code
    def calculate_lane_positions(self, center_pos, neighbor_pos):
        # Calculate the vector representing the edge
        edge_vector = np.array(neighbor_pos) - np.array(center_pos)

        # Calculate the unit vector perpendicular to the edge
        perpendicular_vector = np.array([-edge_vector[1], edge_vector[0]]) / self.GRID_SIZE
        perpendicular_vector = perpendicular_vector * self.LANE_WIDTH / 2

        # Calculate the positions of the two lanes
        towards_lane_st = center_pos + perpendicular_vector
        towards_lane_end = neighbor_pos + perpendicular_vector
        from_lane_st = center_pos - perpendicular_vector
        from_lane_end = neighbor_pos - perpendicular_vector
        return towards_lane_st, towards_lane_end, from_lane_st, from_lane_end

    def draw_agents(self, win):
        visited = set()
        for i, vertex in enumerate(self.graph):
            center_pos = self.convert_grid_loc_to_pixel(np.array(vertex))
            # pygame.draw.circle(win, Color.WHITE, center_pos, 10, 3)

            # text = len(self.graph[vertex])
            # win.blit(default_font.render(str(text), True, pygame.Color("white"), (28, 28, 28)), center_pos - 25)

            for neighbor in self.graph[vertex]:
                if (vertex, neighbor) in visited:
                    continue
                visited.add((vertex, neighbor))
                visited.add((neighbor, vertex))
                neighbor_pos = self.convert_grid_loc_to_pixel(np.array(neighbor))
                pygame.draw.line(win, Color.STEEL_BLUE, tuple(center_pos), tuple(neighbor_pos), 2 * self.LANE_WIDTH)
                pygame.draw.line(win, Color.CULTURED, tuple(center_pos), tuple(neighbor_pos), 1)

            chonk = 50
            junction_rect = (center_pos[0] - chonk / 2, center_pos[1] - chonk / 2), (
                chonk,
                chonk,
            )
            # pygame.draw.rect(win, Color.CULTURED, junction_rect)

        for path in self.paths:
            path.draw(win)

        for car in self.cars:
            self.check_collision(car, win)
            if car.tracker.ended is False:
                car.draw(win)
                # self.cars.remove(car)

        for junction in self.junctions:
            junction.draw(win, self.cars)

        stats.add(cars=len(self.cars))

    def check_collision(self, car: IDMCar, win):
        line = np.arange(car.height - 1, self.LANE_WIDTH * 2, car.height / 2, dtype=np.int32)
        x, y = (
            line * np.cos(np.radians(car.angle + 180)) + car.x,
            line * np.sin(np.radians(car.angle + 180)) + car.y,
        )
        for point in np.array([x, y]).T:
            # pygame.draw.circle(win, Color.RED, point, 5, 1)
            for other_car in self.cars:
                if car != other_car and other_car.rotated_car_rect.collidepoint(point):
                    return car.collides_with(other_car.x, other_car.y, other_car.velocity)

    def end_simulation_save(self):
        # code to save to csv

        df = pd.DataFrame([tracker.__dict__ for tracker in self.trackers])

        df.drop(
            columns=[
                "path",
                "next_car_tracker",
                "ended",
                "target_x",
                "target_y",
                "tracker",
            ],
            inplace=True,
        )
        print(df.columns)
        name = "roundabout"

        df.to_csv(f"{name}-{time.time()}.csv", mode="w", index=False)

    def end_run_and_reset(self):
        last_time = pygame.time.get_ticks()
        travel_times = []
        for car in self.cars:
            if car.tracker.ended:
                travel_times.append(car.tracker.end_time - car.tracker.start_time)

        total_travel_time = mean(travel_times)
        print("Total travel time \t ",total_travel_time/1000)

        self.init_paths(20)
        self.cars = []
