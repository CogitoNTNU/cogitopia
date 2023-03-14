"""Earth layer."""
import numpy as np

from .layer import Layer

class Clouds(Layer):
    def __init__(self, grid_width,grid_height, initial, world):
        Layer.__init__(self, grid_width,grid_height, initial, world)
        self.grid.fill(0)
        self.grid[5, 5] = 1

    def create_cloud(self,x_pos,y_pos):
        self.grid[x_pos, y_pos] = 1

    def step(self):
        if np.random.randint(0,100) > 95:
            self.create_cloud(np.random.randint(0,self.grid_width),np.random.randint(self.grid_height))

        temp_grid = self.grid.copy()
        rand = np.random.randint(0,5)/100
        self.grid += np.roll(self.grid,1)*rand
        self.grid -= temp_grid*rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(temp_grid, -1) * rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(self.grid, 1,axis = 0) * rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(temp_grid, -1, axis = 0) * rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(temp_grid, 1, axis=(0,1)) * rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(np.roll(temp_grid, 1, axis=0),-1,axis=-1)*rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(np.roll(temp_grid, -1, axis=0), 1, axis=-1) * rand
        self.grid -= temp_grid * rand
        rand = np.random.randint(0, 5) / 100
        self.grid += np.roll(temp_grid, -1, axis=(0,1)) * rand
        self.grid -= temp_grid * rand

        rng = np.random.default_rng()
        self.grid = np.roll(self.grid, 1-rng.integers(0,3,dtype=int), axis=np.random.randint(2, size=2))


        self.grid -= 0.0012  # 0.012
        self.grid = np.clip(self.grid, 0, 1)









    @staticmethod
    def get_color(value):
        return 140+100*(0.5-value), 140+100*(0.5-value), 140+100*(0.5-value)
