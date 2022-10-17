import numpy as np


class Layer:
    def __init__(self, size, initial):
        self.size = size
        self.grid = np.array(initial)

    def get_layer(self):
        return self.grid

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, value, x, y):
        self.grid[x][y] = value

    def get_neighbors(self, i, j):
        neighbors = np.zeros((8, 2), dtype=np.dtype('i2'))
        neighbors[7] = [(i + 1) % self.size, (j - 1) % self.size]
        neighbors[6] = [(i - 1) % self.size, (j - 1) % self.size]
        neighbors[5] = [(i - 1) % self.size, (j + 1) % self.size]
        neighbors[4] = [(i + 1) % self.size, (j + 1) % self.size]
        neighbors[3] = [i, (j + 1) % self.size]
        neighbors[1] = [i, (j - 1) % self.size]
        neighbors[2] = [(i + 1) % self.size, j]
        neighbors[0] = [(i - 1) % self.size, j]
        return neighbors
