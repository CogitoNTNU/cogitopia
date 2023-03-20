import numpy as np

from .layer import Layer


class MoveableWater(Layer):
    def __init__(self, grid_width,grid_height, initial, world):
        Layer.__init__(self, grid_width,grid_height, initial, world)
        self.grid.fill(0)
        self.grid[5,5] = 1
        self.amount = 1

    def step(self):
        #self.world.clouds.grid
        y, x = np.nonzero(self.grid)
        for i in range(len(y)):
            flow_to =  np.argmin(self.world.height.grid[y[i]-1:(y[i]+1)%self.world.grid_height,x[i]-1:(x[i]+1)%self.world.grid_width])
            flow_to = np.unravel_index(flow_to, (3,3), order='C')
            self.grid[y[i],x[i]] -= 0.1
            self.grid[flow_to[0]+y[i], flow_to[1]+x[i]] += 0.1
        self.grid = np.clip(self.grid, 0, 1)






    @staticmethod
    def get_color(value):
        return 0, 0, value * 180 + 50
