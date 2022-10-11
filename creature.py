import pygame
import numpy as np
from random import randrange
import random
from world import World

grid_size = 20
(N, W, S, E) = [0, 1, 2, 3]


class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = randrange(3)

    def turn(self):
        turning = np.random.randint(0, 3)
        if self.d == 1 and turning == 2:
            self.d = W
        elif self.d == 4 and turning == 1:
            self.d = N
        elif turning == 2:
            self.d = self.d - 1 % 4
        else:
            self.d = self.d + turning % 4

    def step(self):
        if self.d == N:
            self.y = (self.y + 1) % grid_size
        elif self.d == S:
            self.y = (self.y - 1) % grid_size
        elif self.d == E:
            self.x = (self.x - 1) % grid_size
        elif self.d == W:
            self.x = (self.x + 1) % grid_size
        elif self.d == 0:
            self.x = self.x
            self.y = self.y

    @staticmethod
    def vision(world):
        np.argwhere(max(world))
