import numpy as np

from .layer import Layer


class MoveableWater(Layer):
    def __init__(self, grid_width,grid_height, initial, world):
        Layer.__init__(self, grid_width,grid_height, initial, world)
        self.grid.fill(0)
        self.grid[19,19] =1
        self.grid[12, 1] = 1
        self.grid[5, 5] = 1
        self.amount = 1

    def step(self):
        flow = 10
        self.grid[7, 7] = 1
        self.grid[8, 8] = 1
        self.grid[7, 8] = 1
        x, y = np.nonzero(self.grid)
        # if np.random.randint(0, 100) > 95:
        #     self.grid += self.world.clouds.grid
        # self.grid -= 0.001
        # grady = np.diff(self.world.height.grid, prepend=self.world.height.grid[0], append=self.world.height.grid[1],axis=0)
        # gradx = np.diff(self.world.height.grid, prepend=self.world.height.grid[:,1], append=self.world.height.grid[:,1],axis=1)
        # self.grid = np.clip(self.grid, 0, 1)
        # flow_to = np.argmin(self.world.height.grid[(x[0]-1):(x[0]+2),(y[0]-1):(y[0]+2)])
        # print(self.world.height.grid[(x[0]-1):(x[0]+2),(y[0]-1):(y[0]+2)])
        # print(flow_to)
        # flow_to = np.unravel_index(flow_to, (3, 3), order='C')
        # print(flow_to)
        # self.grid[flow_to[0]+x[0]+1,flow_to[1]+y[0]+1] += 1

        for i in range(len(y)):
                dict_dir = np.array([[ (x[i] - 1) % self.world.grid_width, y[i] % self.world.grid_height],[(x[i]+1) % self.world.grid_width, y[i] % self.world.grid_height],
                            [(x[i]) % self.world.grid_width, (y[i]-1) % self.world.grid_height],[(x[i]) % self.world.grid_width, (y[i] + 1) % self.world.grid_height],
                                     [x[i], y[i]],[
                                      (x[i] + 1) % self.world.grid_width, (y[i]+1) % self.world.grid_height], [
                                      (x[i]+1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height],
                                     [(x[i] - 1) % self.world.grid_width, (y[i] + 1) % self.world.grid_height],
                                     [
                                         (x[i] - 1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height]

                                     ] )
                temp =  np.zeros(9)
                ini_sum = np.sum(self.grid)
                temp[0] = (self.world.height.grid[(x[i]-1)%self.world.grid_width,y[i]%self.world.grid_height]- self.world.height.grid[x[i],y[i]])*flow
                temp[1] = (
                    self.world.height.grid[(x[i] +1) % self.world.grid_width, y[i] % self.world.grid_height] -
                    self.world.height.grid[x[i], y[i]])*flow
                temp[2] =  (
                    self.world.height.grid[(x[i] ) % self.world.grid_width, (y[i]-1) % self.world.grid_height] -
                    self.world.height.grid[x[i], y[i]])*flow
                temp[3] =(self.world.height.grid[(x[i]) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -
                    self.world.height.grid[x[i], y[i]])*flow
                temp[4] = (
                    self.world.height.grid[(x[i]) % self.world.grid_width, (y[i]) % self.world.grid_height] -
                    self.world.height.grid[x[i], y[i]])*flow
                temp[5] = (
                                  self.world.height.grid[
                                      (x[i] + 1) % self.world.grid_width, (y[i]+1) % self.world.grid_height] -
                                  self.world.height.grid[x[i], y[i]]) * flow
                temp[6] = (
                                  self.world.height.grid[
                                      (x[i]+1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height] -
                                  self.world.height.grid[x[i], y[i]]) * flow
                temp[7] = (self.world.height.grid[(x[i]-1) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -
                           self.world.height.grid[x[i], y[i]]) * flow
                temp[8] = (self.world.height.grid[
                               (x[i] - 1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height] -
                           self.world.height.grid[x[i], y[i]]) * flow





                dir = np.argmin(temp)

                # temp = np.clip(temp, 0, 1)
                # temp[(x[i]-1)%self.world.grid_width,y[i]%self.world.grid_height] -= \
                #     np.clip(self.world.height.grid[(x[i]-1)%self.world.grid_width,y[i]%self.world.grid_height]- self.world.height.grid[x[i],y[i]],-1,0)*flow
                # temp[(x[i]+1) % self.world.grid_width, y[i] % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i] +1) % self.world.grid_width, y[i] % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i]) % self.world.grid_width, (y[i]-1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i] ) % self.world.grid_width, (y[i]-1) % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i]) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i]) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i]+1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i]+1) % self.world.grid_width, (y[i] - 1) % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i]+1) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i]+1) % self.world.grid_width, (y[i] + 1) % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i] - 1) % self.world.grid_width, (y[i]-1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i] - 1) % self.world.grid_width, (y[i]-1) % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                # temp[(x[i] + 1) % self.world.grid_width, (y[i]+1) % self.world.grid_height] -= np.clip(
                #     self.world.height.grid[(x[i] + 1) % self.world.grid_width, y[i] % self.world.grid_height] -
                #     self.world.height.grid[x[i], y[i]], -1, 0)*flow
                self.grid[dict_dir[dir,0],dict_dir[dir,1]] -= np.min(temp)
                self.grid[x[i],y[i]]-=abs(ini_sum-np.sum(self.grid))

        self.grid = np.clip(self.grid, 0, 1)





    @staticmethod
    def get_color(value):
        return 0, 0, value * 180 + 50
