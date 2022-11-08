from random import randrange

import numpy as np


class Creature:
    N, E, S, W = range(4)
    EAT, TURN_L, TURN_R, WALK, STAY, DIE = range(6)
    RIGHT, LEFT = range(2)
    ID_COUNTER = 0

    def __init__(self, x, y, world, color):
        self.x = x
        self.y = y
        self.d = randrange(4)
        self.grid_size = world.size
        self.action_buffer = None
        self.world = world
        self.food = .5
        self.color = color
        self.inf_loop = False
        self.id = Creature.ID_COUNTER
        self.agent_type = None
        Creature.ID_COUNTER += 1

    def request_action(self, action):
        if action in range(6):
            self.action_buffer = action
            return True
        return False

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
        if self.action_buffer == Creature.DIE:
            self.inf_loop = True
        
        if self.food > 0.9:
            self.world.reproduction_callback(self)
            self.food -= 0.5
        
        self.food -= 0.02

    def turn(self, direction):  # direction 0 = right, 1 = left
        if direction == Creature.RIGHT:
            self.d = (self.d + 1) % 4
        if direction == Creature.LEFT:
            self.d = (self.d - 1) % 4

    def walk(self):
        if self.d == self.N:
            self.y = (self.y - 1) % self.grid_size
        elif self.d == self.S:
            self.y = (self.y + 1) % self.grid_size
        elif self.d == self.E:
            self.x = (self.x + 1) % self.grid_size
        elif self.d == self.W:
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
        if self.d == self.N:
            return self.x, (self.y - 1) % self.grid_size
        if self.d == self.S:
            return self.x, (self.y + 1) % self.grid_size
        if self.d == self.E:
            return (self.x + 1) % self.grid_size, self.y
        return (self.x - 1) % self.grid_size, self.y

    def get_food(self):
        return self.food

    def get_color(self):
        return self.color

    def get_inf_loop(self):
        return self.inf_loop
