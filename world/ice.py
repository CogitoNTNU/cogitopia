"""Water layer."""
import numpy as np

from .layer import Layer


class Ice(Layer):

    def __init__(self, grid_width, grid_height,initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)
        self.grid.fill(0)
    def step(self):
        #if  (self.world.time % 4):
        self.grid = np.clip(0.1-self.world.temperature.grid,0,1) #*self.world.water.grid

    @staticmethod
    def get_color(value):
        return 200, 200, 244