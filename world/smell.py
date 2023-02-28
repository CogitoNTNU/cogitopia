"""Earth layer."""
import numpy as np

from .layer import Layer

class Smell(Layer):
    def __init__(self, grid_width,grid_height, initial, world):
        Layer.__init__(self, grid_width,grid_height, initial, world)
        self.grid.fill(0)
        self.grid[5, 5] = 1

    def create_smell(self,x_pos,y_pos):
        self.grid[x_pos, y_pos] = 1

    def step(self):
        temp_grid = self.grid.copy()
        self.grid += np.roll(self.grid,1)*0.01
        self.grid -= temp_grid*0.01
        self.grid += np.roll(temp_grid, -1) * 0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(self.grid, 1,axis = 0) * 0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(temp_grid, -1, axis = 0) * 0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(temp_grid, 1, axis=(0,1)) * 0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(np.roll(temp_grid, 1, axis=0),-1,axis=-1)*0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(np.roll(temp_grid, -1, axis=0), 1, axis=-1) * 0.01
        self.grid -= temp_grid * 0.01
        self.grid += np.roll(temp_grid, -1, axis=(0,1)) * 0.01
        self.grid -= temp_grid * 0.01


        self.grid -= 0.001  # 0.012
        self.grid = np.clip(self.grid, 0, 1)



        self.grid = np.clip(self.grid, 0, 1)







    @staticmethod
    def get_color(value):
        return value * 100 +50, 50, 100
