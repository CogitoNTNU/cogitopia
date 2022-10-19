import numpy as np

from .layer import Layer


class Water(Layer):

    def __init__(self, size, height_layer):
        initial = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                height = height_layer.get_value(i, j)
                if height < 0.05:
                    initial[i][j] = 0.05 - height
        Layer.__init__(self, size, initial)

    @staticmethod
    def get_color(value):
        return 0, 0, value * 2000 + 50

    def is_water(self, x, y):
        return self.get_value(x, y) > 0
