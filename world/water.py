"""Water layer."""
import numpy as np

from .layer import Layer


class Water(Layer):

    def __init__(self, size, height_layer, world):
        initial = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                height = height_layer.get_value(i, j)
                if height < 0.05:
                    initial[i][j] = 0.05 - height
        Layer.__init__(self, size, initial, world)

        for i in range(self.size):
            for j in range(self.size):
                if self.is_water(i, j):
                    self.world.grass.set_value(0, i, j)
                    self.world.earth.set_value(0, i, j)

    @staticmethod
    def get_color(value):
        return 0, 0, value * 2000 + 50

    def is_water(self, x, y):
        return self.get_value(x % self.world.size, y % self.world.size) > 0
