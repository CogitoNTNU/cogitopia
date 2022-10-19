import numpy as np

from .layer import Layer


class Sun(Layer):
    def __init__(self, size, world):
        initial = np.zeros((size, size))
        Layer.__init__(self, size, initial, world)

    def step(self, time):
        for i in range(len(self.grid)):
            self.grid[i].fill(abs(np.cos(time / 24 * 2 * np.pi + i * np.pi / self.size)))

    @staticmethod
    def get_color(value):
        return value * 200, value * 200, 0
