from random import randrange

import numpy as np

N, E, S, W = range(4)
LEFT, RIGHT, FORWARD = range(3)


class Creature:
    EAT, TURN_L, TURN_R, WALK = range(4)

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.d = randrange(3)
        self.grid_size = size

    def turn(self):
        turning = np.random.choice([LEFT, RIGHT, FORWARD])
        if turning == RIGHT:
            self.d = (self.d - 1) % 4
        elif turning == LEFT:
            self.d = (self.d + 1) % 4

    def walk(self):
        if self.d == N:
            self.y = (self.y + 1) % self.grid_size
        elif self.d == S:
            self.y = (self.y - 1) % self.grid_size
        elif self.d == E:
            self.x = (self.x - 1) % self.grid_size
        elif self.d == W:
            self.x = (self.x + 1) % self.grid_size
        elif self.d == 0:
            self.x = self.x
            self.y = self.y

    def vision(self, world):
        grass = np.zeros(9)
        grass[0] = world.get_grass(self.x - 1, self.y - 1)
        grass[1] = world.get_grass(self.x, self.y - 1)
        grass[2] = world.get_grass(self.x + 1, self.y - 1)
        grass[3] = world.get_grass(self.x - 1, self.y)
        grass[4] = world.get_grass(self.x, self.y)
        grass[5] = world.get_grass(self.x + 1, self.y)
        grass[6] = world.get_grass(self.x - 1, self.y + 1)
        grass[7] = world.get_grass(self.x, self.y + 1)
        grass[8] = world.get_grass(self.x + 1, self.y + 1)
        grass = grass.reshape(3, 3)
        return np.unravel_index(grass.argmax(), grass.shape)


'''
    def move_towards(self, world):
        max = self.vision(world)
'''
