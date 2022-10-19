import numpy as np

from .layer import Layer


class Grass(Layer):
    def __init__(self, size, initial, world):
        Layer.__init__(self, size, initial, world)

    def step(self):
        self.grid += self.world.earth.get_layer() * 0.005 * 0.2
        self.grid = np.clip(self.grid, 0, 1)

    def eat_grass(self, x, y):
        amount = self.get_value(x, y)
        self.set_value(0, x, y)
        return amount

    @staticmethod
    def get_color(value):
        return 0, 150 * value + 45, 0
