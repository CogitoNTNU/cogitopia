import pygame
from random import randrange
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise

class world:
    griddepth = 10
    grid = None
    gridsize = None
    def __init__(self,gridsize):
        world.gridsize = gridsize
        xpix, ypix = gridsize, gridsize
        world.grid = np.full((world.griddepth, xpix, ypix), None)
        world.initialize_grass(self)
        world.initialize_earth(self)

    def initialize_grass(self):
        noise = PerlinNoise(octaves=5, seed=10)
        xpix, ypix = world.gridsize, world.gridsize
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]
        for j in range(xpix):
            for i in range(ypix):
                world.grid[0][j][i] = abs(pic[j][i]) * 180 + 75
    def initialize_earth(self):
        world.grid[1].fill(100)
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
