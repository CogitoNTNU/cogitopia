import random

import numpy as np

from .layer import Layer
import scipy


class Flowers(Layer):
    def __init__(self, grid_width, grid_height, initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)
        self.grid.fill(0)
        #self.grid = np.clip(self.grid,0,1)
        for i in range(40):
            self.grid[np.random.randint(0,self.grid_width),np.random.randint(self.grid_height)] = 1 #np.random.randint(1,10)/10
    def step(self):


        for i in range(self.grid_width):
            for j in range(self.grid_height):
                if self.world.water.is_water(i, j):
                    self.grid[i][j] = 0
        pass

    @staticmethod
    def get_color(value):
        return 200 * value + 45,0, 0

    @staticmethod
    def get_second_color(value):
        return 200 * value +45,200 * value +45, 200 * value +45