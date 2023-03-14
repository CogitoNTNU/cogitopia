import numpy as np

from .layer import Layer


class Sun(Layer):
    def __init__(self, grid_width, grid_height, world):
        initial = np.zeros((grid_width, grid_height))
        Layer.__init__(self, grid_width, grid_height, initial, world)

    def step(self, time):
        mu = self.world.grid_height / 2
        sigma = self.world.grid_height/ 4

        for i in range(self.world.grid_width):
            self.grid[i] = (np.cos(time / 24 * 2 * np.pi + (i) * 2 * np.pi / self.world.grid_width) + 0.3)

        for i in range(self.world.grid_height):
            self.grid[:,i] *= 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((i - mu) / (sigma)) ** 2 * 0.5) * 10

        self.grid = np.clip(self.grid, 0, 1)

    @staticmethod
    def get_color(value):
        return value * 200, value * 200, 0
