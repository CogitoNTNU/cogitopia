import numpy as np

from .layer import Layer
import scipy

class Grass(Layer):
    def __init__(self, grid_width, grid_height, initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)
    def step(self):
        self.grid += 0.005 * self.world.sun.grid * self.world.settings.grass_growth_rate
        #self.grid += (1 - (self.world.earth.grid) * 0.005)
        self.world.earth.grid -=0.005 * self.world.sun.grid * self.world.settings.grass_growth_rate
        self.grid = np.clip(self.grid, 0, self.world.earth.grid)
        if self.world.settings.use_temp: self.grid -= ((abs(self.world.temperature.grid - 0.5) - (self.world.temperature.grid - 0.5)) )* 0.005
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.world.water.is_water(i, j):
                    self.grid[i][j] = 0
        #self.grid = scipy.ndimage.convolve(self.grid,[[0.1,0.1,0.1],[0.1,0.2,0.1],[0.1,0.1,0.1]])
        #self.grid = scipy.ndimage.convolve(self.grid, [[ 0.25, 0.25], [ 0.25, 0.25]])*1.2
        self.grid = np.clip(self.grid, 0, 1)

    def eat_grass(self, x, y):
        amount = self.get_value(x, y)
        self.set_value(0, x, y)
        return amount

    @staticmethod
    def get_color(value):
        return 0, 150 * value + 45, 0
