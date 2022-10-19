from random import randrange

import numpy as np

N, E, S, W = range(4)


class Creature:
    EAT, TURN_L, TURN_R, WALK = range(4)
    RIGHT, LEFT = range(2)

    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.d = randrange(4)
        self.grid_size = world.size
        self.action_buffer = None
        self.world = world
        self.food = 1

    def request_action(self, action):
        self.action_buffer = action

        if self.action_buffer == Creature.WALK:
            x1, y1 = self.front()
            if self.world.water.get_value(x1, y1) > 0:
                return False

        if self.action_buffer == Creature.EAT:
            if self.world.grass.get_value(self.x, self.y) < 0.05:
                return False

        return True

    def process_action(self):
        if self.action_buffer == Creature.EAT:
            amount = self.world.grass.eat_grass(self.x, self.y)
            self.food += amount
            self.food = np.clip(self.food, -1, 1)
        if self.action_buffer == Creature.TURN_L:
            self.turn(Creature.LEFT)
        if self.action_buffer == Creature.TURN_R:
            self.turn(Creature.RIGHT)
        if self.action_buffer == Creature.WALK:
            self.walk()

        self.food -= 0.02

    def turn(self, direction):  # direction 0 = right, 1 = left
        if direction == Creature.RIGHT:
            self.d = (self.d + 1) % 4
        if direction == Creature.LEFT:
            self.d = (self.d - 1) % 4

    def walk(self):
        if self.d == N:
            self.y = (self.y + 1) % self.grid_size
        elif self.d == S:
            self.y = (self.y - 1) % self.grid_size
        elif self.d == E:
            self.x = (self.x + 1) % self.grid_size
        elif self.d == W:
            self.x = (self.x - 1) % self.grid_size

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

    def front(self):
        if self.d == N:
            return self.x, (self.y + 1) % self.grid_size
        elif self.d == S:
            return self.x, (self.y - 1) % self.grid_size
        elif self.d == E:
            return (self.x + 1) % self.grid_size, self.y
        else:
            return (self.x - 1) % self.grid_size, self.y

    def get_food(self):
        return self.food
