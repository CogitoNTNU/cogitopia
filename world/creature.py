from random import randrange, choice

import numpy as np


class Creature:
    N, E, S, W = range(4)
    EAT, TURN_L, TURN_R, WALK, STAY, DIE, REPRODUCE, KILL = range(8)
    RIGHT, LEFT = range(2)
    ID_COUNTER = 0

    def __init__(self, x, y, world, color, predator):
        self.x = x
        self.y = y
        self.d = randrange(4)
        self.action_buffer = None
        self.world = world
        self.food = 0.4
        self.meat = 10
        self.color = color
        self.is_dead = False
        self.id = Creature.ID_COUNTER
        self.agent_type = None
        Creature.ID_COUNTER += 1
        self.predator = predator

    def request_action(self, action):
        if action in range(8):
            self.action_buffer = action
            return True
        return False

    def process_action(self):
        if self.is_dead:
            return
        if self.action_buffer == Creature.EAT:
            if self.predator:
                amount = self.eat_meat(1 - self.food)
            else:
                amount = self.world.grass.eat_grass(self.x, self.y)
            self.food += amount
            self.food = np.clip(self.food, -1, 1)
        if self.action_buffer == Creature.TURN_L:
            self.turn(Creature.LEFT)
            self.food -= 0.0005
        if self.action_buffer == Creature.TURN_R:
            self.turn(Creature.RIGHT)
            self.food -= 0.0005
        if self.action_buffer == Creature.WALK:
            self.world.creatures_array[self.x][self.y].remove(self)
            self.walk()
            self.world.creatures_array[self.x][self.y].append(self)
            if self.world.water.is_water(self.x, self.y):
                self.food -= 0.008
            self.food -= 0.002
        if self.action_buffer == Creature.REPRODUCE:
            self.world.reproduction_callback(self)
            self.food -= 0.5
        if self.action_buffer == Creature.KILL:
            if self.predator:
                self.kill()
                self.food -= 0.3
        self.food -= 0.0002
        self.action_buffer = None

    def turn(self, direction):  # direction 0 = right, 1 = left
        if direction == Creature.RIGHT:
            self.d = (self.d + 1) % 4
        if direction == Creature.LEFT:
            self.d = (self.d - 1) % 4

    def walk(self):
        if self.d == self.N:
            self.y = (self.y - 1) % self.world.grid_height
        elif self.d == self.S:
            self.y = (self.y + 1) % self.world.grid_height
        elif self.d == self.E:
            self.x = (self.x + 1) % self.world.grid_width
        elif self.d == self.W:
            self.x = (self.x - 1) % self.world.grid_width

    def kill(self):
        creature = self
        while creature != self and creature.is_dead:
            creature = choice(self.world.get_creatures_at_location(self.x, self.y))
        creature.is_dead = True
        print("KILL!")

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
            return self.x, (self.y - 1) % self.grid_height
        if self.d == self.S:
            return self.x, (self.y + 1) % self.grid_height
        if self.d == self.E:
            return (self.x + 1) % self.grid_width, self.y
        return (self.x - 1) % self.grid_width, self.y

    def get_food(self):
        return self.food

    def get_color(self):
        return self.color

    def remove_from_array(self):
        self.world.creatures_array[self.x][self.y].remove(self)

    def eat_meat(self, amount):
        for creature in self.world.get_creatures_at_location(self.x, self.y):
            if creature != self and creature.is_dead:
                eaten = min(amount, creature.meat)
                creature.meat -= amount
                return eaten
        return 0
