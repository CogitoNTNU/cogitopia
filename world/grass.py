import numpy as np

from .layer import Layer


class Grass(Layer):
    def __init__(self, grid_width, grid_height, initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)

    def step(self):
        self.grid += 0.005 * self.world.sun.grid * self.world.settings.grass_growth_rate
        self.grid *= (1 - (self.world.earth.grid) * 0.005)
        if self.world.settings.use_temp: self.grid -= ((abs(self.world.temperature.grid - 0.5) - (self.world.temperature.grid - 0.5)) )* 0.005
        self.grid = np.clip(self.grid, 0, 1)

    def eat_grass(self, x, y):
        amount = self.get_value(x, y)
        self.set_value(0, x, y)
        return amount

    @staticmethod
    def get_color(value):
        return 0, 150 * value + 45, 0
