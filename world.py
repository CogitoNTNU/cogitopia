import pygame
from random import randrange
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise

class world:
    griddepth = 10
    grid = None
    gridsize = None
    time = 0
    def __init__(self,gridsize):
        world.gridsize = gridsize
        xpix, ypix = gridsize, gridsize
        world.grid = np.full((world.griddepth, xpix, ypix), None)
        world.initialize_grass(self)
        world.initialize_earth(self)
        world.initialize_temp(self)
        world.initialize_heigh(self)
        world.initialize_water(self)
        world.initialize_sun_intensity(self)

    def step_time(self,stepsize=1):
        world.time = (world.time + stepsize) % 24

    def initialize_grass(self):
        noise = PerlinNoise(octaves=5, seed=10)
        xpix, ypix = world.gridsize, world.gridsize
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
        for j in range(xpix):
            for i in range(ypix):
                world.grid[0][j][i] = abs(pic[j][i])
    def step_grass(self,stepsize = 0.005):
        world.grid[0] += world.grid[1]*stepsize
        #world.grid[0]*=(1-abs(world.grid[0]-world.grid[1]))
        world.grid[0] = np.clip(world.grid[0],0,1)
        world.step_earth(self)


    def get_grass(self, x, y):
        return self.grid[0][x][y]


    def eat_grass(self, x, y):
        amount = self.grid[0]
        self.grid[0][x][y] = 0
        return amount


    def step_earth(self,stepsize = 0.1):
        world.grid[1]*=(1-(world.grid[0])*stepsize)
        world.grid[1]+=stepsize*0.005
        world.grid[1] = np.clip(world.grid[1], 0, 1)
    def initialize_earth(self):
        noise = PerlinNoise(octaves=5, seed=10)
        xpix, ypix = world.gridsize, world.gridsize
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
        for j in range(xpix):
            for i in range(ypix):
                world.grid[1][j][i] = abs(pic[j][i])

    def get_earth(self, x, y):
        return self.grid[1][x][y]

    def initialize_temp(self):
        noise = PerlinNoise(octaves=5, seed=10)
        xpix, ypix = world.gridsize, world.gridsize
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
        for j in range(xpix):
            for i in range(ypix):
                world.grid[3][j][i] = abs(pic[j][i])


    def get_temp(self, x, y):
        return self.grid[3][x][y]


    def initialize_heigh(self):
        noise = PerlinNoise(octaves=5, seed=10)
        xpix, ypix = world.gridsize, world.gridsize
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
        for j in range(xpix):
            for i in range(ypix):
                world.grid[4][j][i] = abs(pic[j][i])

    def get_height(self, x, y):
        return self.grid[4][x][y]

    def initialize_water(self):
        world.grid[2].fill(0)
        world.grid[2][2][2]=1
        world.grid[2][1][0]=1


    def get_water(self, x, y):
        return self.grid[2][x][y]

    def initialize_sun_intensity(self):
        world.grid[5].fill(0)

    def step_water(self):
        for j in range(world.gridsize):
            for i in range(world.gridsize):
                if world.grid[2][j][i] != 0:
                    for neighbor in world.neighborPoints(self,i,j):
                        if world.grid[4][neighbor[0]][neighbor[1]]- world.grid[4][j][i] < 0:
                            world.grid[2][neighbor[0]][neighbor[1]] += 0.01*(1-world.grid[2][neighbor[0]][neighbor[1]])
                            world.grid[2][j][i] -= 0.01*(1-world.grid[2][neighbor[0]][neighbor[1]])
                            world.grid[2] = np.clip(world.grid[2], 0, 1)
    def step_temp(self):
        for j in range(world.gridsize):
            for i in range(world.gridsize):
                    for neighbor in world.neighborPoints(self,i,j):
                        if world.grid[3][neighbor[0]][neighbor[1]]- world.grid[3][j][i] < 0:
                            world.grid[3][neighbor[0]][neighbor[1]] += 0.01*(1-world.grid[3][neighbor[0]][neighbor[1]])
                            world.grid[3][j][i] -= 0.01*(1-world.grid[3][neighbor[0]][neighbor[1]])
                            world.grid[3] = np.clip(world.grid[3], 0, 1)
    def step_sun(self):
        world.grid[5].fill(world.time)


    def get_grid(self):
        return world.grid
    def neighborPoints(self, i, j):
        neighbors = np.zeros((8, 2), dtype=np.dtype('i2'))
        neighbors[7] = [(i + 1) % world.gridsize, (j - 1) % world.gridsize]
        neighbors[6] = [(i - 1) % world.gridsize, (j - 1) % world.gridsize]
        neighbors[5] = [(i-1)%world.gridsize, (j+1)%world.gridsize]
        neighbors[4] = [(i+1)%world.gridsize, (j+1)%world.gridsize]
        neighbors[3] = [i, (j+1)%world.gridsize]
        neighbors[1] = [i, (j-1)%world.gridsize]
        neighbors[2] = [(i+1)%world.gridsize, j]
        neighbors[0] = [(i-1)%world.gridsize, j]
        return neighbors
