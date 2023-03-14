import numpy as np

from .layer import Layer


class Temperature(Layer):
    def __init__(self, grid_width,grid_height, initial, world):
        Layer.__init__(self, grid_width,grid_height, initial, world)

    def step(self):
        temp_grid = self.grid.copy()
        temp_grid = np.c_[temp_grid,temp_grid[:,0]]
        diff = np.diff(temp_grid,axis = 1)
        self.grid += 0.1*(diff)
        temp_grid = self.grid.copy()
        temp_grid = np.r_[temp_grid, [temp_grid[0]]]
        diff = np.diff(temp_grid, axis = 0)
        self.grid += 0.1*(diff)
        self.grid += 0.1 * self.world.sun.grid
        self.grid -= 0.06 *self.world.height.grid
        self.grid -= 0.005
        self.grid = np.clip(self.grid, 0, 1)





    @staticmethod
    def get_color(value):
        return value * 100 , 0, 0
