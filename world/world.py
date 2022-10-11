import pygame
from numpy import random
from random import randrange
import numpy as np
from perlin_noise import PerlinNoise


class World:
    grid_depth = 10
    grid = None
    grid_size = None
    time = 0

    def __init__(self, grid_size):
        World.grid_size = grid_size
        x_pix, y_pix = grid_size, grid_size
        World.grid = np.full((World.grid_depth, x_pix, y_pix), None)
        World.initialize_grass(self)
        World.initialize_earth(self)
        World.initialize_temp(self)
        World.initialize_heigh(self)
        World.initialize_water(self)
        World.initialize_sun_intensity(self)

    def step_time(self, step_size=1):
        World.time = (World.time + step_size) % 24

    def initialize_grass(self):
        noise = PerlinNoise(octaves=5, seed=10)
        x_pix, y_pix = World.grid_size, World.grid_size
        pic = [[noise([i / x_pix, j / y_pix]) for j in range(x_pix)] for i in range(y_pix)]
        for j in range(x_pix):
            for i in range(y_pix):
                World.grid[0][j][i] = abs(pic[j][i])

    def step_grass(self, step_size=0.005):
        World.grid[0] += World.grid[1] * step_size * 10
        # World.grid[0]*=(1-abs(World.grid[0]-World.grid[1]))
        World.grid[0] = np.clip(World.grid[0], 0, 1)
        World.step_earth(self)

    def get_grass(self, x, y):
        return self.grid[0][x][y]

    def eat_grass(self, x, y):
        amount = self.grid[0]
        self.grid[0][x][y] = 0
        return amount

    def step_earth(self, step_size=0.1):
        World.grid[1] *= (1 - (World.grid[0]) * step_size)
        World.grid[1] += step_size * 0.005
        World.grid[1] = np.clip(World.grid[1], 0, 1)

    def initialize_earth(self):
        noise = PerlinNoise(octaves=5, seed=10)
        x_pix, y_pix = World.grid_size, World.grid_size
        pic = [[noise([i / x_pix, j / y_pix]) for j in range(x_pix)] for i in range(y_pix)]
        for j in range(x_pix):
            for i in range(y_pix):
                World.grid[1][j][i] = abs(pic[j][i])

    def get_earth(self, x, y):
        return self.grid[1][x][y]

    def initialize_temp(self):
        noise = PerlinNoise(octaves=5, seed=10)
        x_pix, y_pix = World.grid_size, World.grid_size
        pic = [[noise([i / x_pix, j / y_pix]) for j in range(x_pix)] for i in range(y_pix)]
        for j in range(x_pix):
            for i in range(y_pix):
                World.grid[3][j][i] = abs(pic[j][i])

    def get_temp(self, x, y):
        return self.grid[3][x][y]

    def initialize_heigh(self):
        noise = PerlinNoise(octaves=5, seed=10)
        x_pix, y_pix = World.grid_size, World.grid_size
        pic = [[noise([i / x_pix, j / y_pix]) for j in range(x_pix)] for i in range(y_pix)]
        for j in range(x_pix):
            for i in range(y_pix):
                World.grid[4][j][i] = abs(pic[j][i])

    def get_height(self, x, y):
        return self.grid[4][x][y]

    def get_height_difference(self, x1, y1, x2, y2):
        height1 = self.grid[4][x1][y1]
        height2 = self.grid[4][x2][y2]
        return height2 - height1

    def initialize_water(self):
        World.grid[2].fill(0)
        World.grid[2][2][2] = 1
        World.grid[2][1][0] = 1

    def get_water(self, x, y):
        return self.grid[2][x][y]

    def initialize_sun_intensity(self):
        World.grid[5].fill(0)

    def step_water(self):
        for j in range(World.grid_size):
            for i in range(World.grid_size):
                if World.grid[2][j][i] != 0:
                    for neighbor in World.neighborPoints(self, i, j):
                        if World.grid[4][neighbor[0]][neighbor[1]] - World.grid[4][j][i] < 0:
                            World.grid[2][neighbor[0]][neighbor[1]] += 0.01 * (
                                    1 - World.grid[2][neighbor[0]][neighbor[1]])
                            World.grid[2][j][i] -= 0.01 * (1 - World.grid[2][neighbor[0]][neighbor[1]])
                            World.grid[2] = np.clip(World.grid[2], 0, 1)

    def step_temp(self):
        for j in range(World.grid_size):
            for i in range(World.grid_size):
                for neighbor in World.neighborPoints(self, i, j):
                    if World.grid[3][neighbor[0]][neighbor[1]] - World.grid[3][j][i] < 0:
                        World.grid[3][neighbor[0]][neighbor[1]] += 0.01 * (1 - World.grid[3][neighbor[0]][neighbor[1]])
                        World.grid[3][j][i] -= 0.01 * (1 - World.grid[3][neighbor[0]][neighbor[1]])
                        World.grid[3] = np.clip(World.grid[3], 0, 1)

    def step_sun(self):
        World.grid[5] = np.transpose(World.grid[5])
        for i in range(len(World.grid[5])):
            World.grid[5][i].fill(np.cos(World.time / 24 * 2 * np.pi + i * np.pi / len(World.grid[5])))
        World.grid[5] = np.transpose(World.grid[5])

    def get_grid(self):
        return World.grid

    def neighborPoints(self, i, j):
        neighbors = np.zeros((8, 2), dtype=np.dtype('i2'))
        neighbors[7] = [(i + 1) % World.grid_size, (j - 1) % World.grid_size]
        neighbors[6] = [(i - 1) % World.grid_size, (j - 1) % World.grid_size]
        neighbors[5] = [(i - 1) % World.grid_size, (j + 1) % World.grid_size]
        neighbors[4] = [(i + 1) % World.grid_size, (j + 1) % World.grid_size]
        neighbors[3] = [i, (j + 1) % World.grid_size]
        neighbors[1] = [i, (j - 1) % World.grid_size]
        neighbors[2] = [(i + 1) % World.grid_size, j]
        neighbors[0] = [(i - 1) % World.grid_size, j]
        return neighbors