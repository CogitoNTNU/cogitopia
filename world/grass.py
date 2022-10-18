import numpy as np

from .layer import Layer


class Grass(Layer):
    def __init__(self, size, initial):
        Layer.__init__(self, size, initial)

    def step(self, growth_factor):
        self.grid += growth_factor * 0.005 * 1
        self.grid = np.clip(self.grid, 0, 1)

    def eat_grass(self, x, y):
        amount = self.get_value(x, y)
        self.set_value(0, x, y)
        return amount

    @staticmethod
    def get_color(value):
        return 0, 150 * value + 45, 0
