"""Water layer."""
import numpy as np

from .layer import Layer


class Water(Layer):

    def __init__(self, grid_width, grid_height, height_layer, world):
        initial = np.zeros((grid_width, grid_height))
        for i in range(grid_width):
            for j in range(grid_height):
                height = height_layer.get_value(i, j)
                if height < 0.05:
                    initial[i][j] = 0.05 - height
        Layer.__init__(self, grid_width, grid_height, initial, world)

        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.is_water(i, j):
                    self.world.grass.set_value(0, i, j)
                    self.world.earth.set_value(0, i, j)

    @staticmethod
    def get_color(value):
        return 0, 0, value * 2000 + 50

    def is_water(self, x, y):
        return self.get_value(x % self.world.grid_width, y % self.world.grid_height) > 0
