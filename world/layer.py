import numpy as np


class Layer:
    def __init__(self, grid_width, grid_height, initial, world):
        self.grid_width = grid_width 
        self.grid_height = grid_height
        self.grid = np.array(initial)
        self.world = world

    def get_layer(self):
        return self.grid

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, value, x, y):
        self.grid[x][y] = value

    def get_neighbors(self, i, j):
        neighbors = np.zeros((8, 2), dtype=np.dtype('i2'))
        neighbors[7] = [(i + 1) % self.grid_width, (j - 1) % self.grid_height]
        neighbors[6] = [(i - 1) % self.grid_width, (j - 1) % self.grid_height]
        neighbors[5] = [(i - 1) % self.grid_width, (j + 1) % self.grid_height]
        neighbors[4] = [(i + 1) % self.grid_width, (j + 1) % self.grid_height]
        neighbors[3] = [i, (j + 1) % self.grid_height]
        neighbors[1] = [i, (j - 1) % self.grid_height]
        neighbors[2] = [(i + 1) % self.grid_width, j]
        neighbors[0] = [(i - 1) % self.grid_width, j]
        return neighbors
