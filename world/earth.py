"""Earth layer."""
import numpy as np

from .layer import Layer


class Earth(Layer):
    """Earth layer provides nutrients to grass layer and modifies growth rate."""
    def __init__(self, grid_width, grid_height, initial, world):
        Layer.__init__(self, grid_width, grid_height, initial, world)
        #self.grid.fill(1)
        self.grid+=0.1
    def step(self):
        """Updates earth layer, removing nutrents? seems to move towards equilibrium"""
        #self.grid *= (1-self.world.grass.grid*0.1 )
        #self.grid += 0.1
        self.grid *= (1-self.world.height.grid)
        self.grid -= 0.1* np.clip(0.5-self.world.temperature.grid,0,1)
        #self.grid -= self.world.grass.grid*2
        self.grid += 0.1*(self.world.time-self.world.time % 200)/(self.world.time+1)
        #self.grid = 1*self.world.height.grid
        self.grid = np.clip(self.grid, 0.1, 1)
        
    @staticmethod
    def get_color(value):
        """Returns color value"""
        return value * 180 + 65, value * 180 + 75, 0
