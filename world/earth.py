"""Earth layer."""
import numpy as np

from .layer import Layer


class Earth(Layer):
    """Earth layer provides nutrients to grass layer and modifies growth rate."""
    def __init__(self, grid_width, grid_height, initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)
        self.grid.fill(1)
    def step(self):
        """Updates earth layer, removing nutrents? seems to move towards equilibrium"""
        self.grid += (self.world.grass.grid - (self.grid)) * 0.4
        #self.grid = 1*self.world.height.grid
        self.grid = np.clip(self.grid, 0, 1)
        
    @staticmethod
    def get_color(value):
        """Returns color value"""
        return value * 180 + 65, value * 180 + 75, 0
