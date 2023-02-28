from random import randrange, choice

import numpy as np

from math import log2

import world.smell


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
        self.food = self.world.settings.creature_starting_food
        self.meat = np.log2(self.food)
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
            self.meat = log2(2**self.meat+amount)
            self.food = np.clip(self.food, -1, 1)
        if self.action_buffer == Creature.TURN_L:
            self.turn(Creature.LEFT)
            self.food -= self.world.settings.turning_food_cost
        if self.action_buffer == Creature.TURN_R:
            self.turn(Creature.RIGHT)
            self.food -= self.world.settings.turning_food_cost
        if self.action_buffer == Creature.WALK:
            self.world.creatures_array[self.x][self.y].remove(self)
            self.walk()
            self.world.creatures_array[self.x][self.y].append(self)
            if self.world.water.is_water(self.x, self.y):
                self.food -= self.world.settings.walking_in_water_cost
            self.food -= self.world.settings.walking_food_cost
        if self.action_buffer == Creature.REPRODUCE:
            self.world.reproduction_callback(self)
            self.food -= self.world.settings.reproduction_cost
        if self.action_buffer == Creature.KILL:
            if self.predator:
                self.kill()
                self.food -= self.world.settings.killing_cost

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
        for creature in self.world.get_creatures_at_location(self.x, self.y):
            if creature != self and not creature.is_dead:
                creature.is_dead = True

    def get_food(self):
        return self.food

    def get_color(self):
        return self.color

    def remove_from_array(self):
        self.world.creatures_array[self.x][self.y].remove(self)

    def eat_meat(self, amount):
        for creature in self.world.get_creatures_at_location(self.x, self.y):
            if creature != self and creature.is_dead:
                eaten = min((amount, creature.meat))
                eaten = max((eaten, 0))
                creature.meat -= amount
                #world.smell.
                if creature.meat < 0:
                    creature.remove_from_array()
                    creature.world.creatures.remove(creature)
                return eaten
        return 0
