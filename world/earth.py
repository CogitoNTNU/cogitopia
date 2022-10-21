import numpy as np

from .layer import Layer


class Earth(Layer):
    def __init__(self, size, initial, world):
        Layer.__init__(self, size, initial, world)

    def step(self):
        self.grid *= (1 - self.grid * 0.005)
        self.grid += 0.005 * 0.005
        self.grid = np.clip(self.grid, 0, 1)

    @staticmethod
    def get_color(value):
        return value * 180 + 65, value * 180 + 75, 0
