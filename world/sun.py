import numpy as np

from .layer import Layer


class Sun(Layer):
    def __init__(self, size, world):
        initial = np.zeros((size, size))
        Layer.__init__(self, size, initial, world)

    def step(self, time):
        mu = len(self.grid[0]) / 2
        sigma = len(self.grid[0]) / 4
        for i in range(len(self.grid)):
            self.grid[i] = (np.cos(time / 24 * 2 * np.pi + (i) * 2 * np.pi / len(self.grid)) + 0.3)

        for i in range(len(self.grid)):
            self.grid[:,i] *= 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((i - mu) / (sigma)) ** 2 * 0.5) * 10

        self.grid = np.clip(self.grid, 0, 1)


    @staticmethod
    def get_color(value):
        return value * 200, value * 200, 0
