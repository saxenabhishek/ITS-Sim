from typing import List
from comet.agent import Light, IDMCar
from comet import Color


class Junction:
    def __init__(self, lights: List[Light]) -> None:
        self.lights = lights
        self.green_light = -1
        self.shift_light()

    def shift_light(self):
        self.green_light = (self.green_light + 1) % len(self.lights)
        for i, light in enumerate(self.lights):
            if i == self.green_light:
                light.color = Color.GREEN
            else:
                light.color = Color.RED

    def draw(self, win, cars: List[IDMCar]):
        for light in self.lights:
            light.check_touched(cars)
            light.draw(win)
