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

    def step_water(self, height):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != 0:
                    for neighbor in self.get_neighbors(i, j):
                        if height.get_height_difference(neighbor[0], neighbor[1], j, i) < 0:
                            self.grid[2][neighbor[0]][neighbor[1]] += 0.01 * (
                                    1 - self.grid[2][neighbor[0]][neighbor[1]])
                            self.grid[2][j][i] -= 0.01 * (1 - self.grid[2][neighbor[0]][neighbor[1]])
                            self.grid[2] = np.clip(self.grid[2], 0, 1)

    @staticmethod
    def get_color(value):
        return 0, 0, value * 50 + 50
