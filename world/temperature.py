import numpy as np

from .layer import Layer


class Temperature(Layer):
    def __init__(self, size, initial, world):
        Layer.__init__(self, size, initial, world)

    def step(self):
        for j in range(self.size):
            for i in range(self.size):
                for neighbor in self.get_neighbors(i, j):
                        rate = 0.1 * ((self.grid[i][j] - self.grid[neighbor[0]][neighbor[1]]))
                        self.grid[neighbor[0]][neighbor[1]] += 0.01 * (1 - self.grid[neighbor[0]][neighbor[1]])
                        self.grid[i][j] -= 0.01 * (1 - self.grid[neighbor[0]][neighbor[1]])
                        self.grid = np.clip(self.grid, 0, 1)
                        self.grid = np.clip(self.grid, 0, 1)
                        self.grid[i][j] -= rate

        self.grid += 0.1 * self.world.sun.grid[5]
        self.grid -= 0.01
        self.grid = np.clip(self.grid, 0, 1)




    @staticmethod
    def get_color(value):
        return value * 100 + 50, 0, 0
