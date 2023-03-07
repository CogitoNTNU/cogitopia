"""Torgeirs (stupid) agent"""
import random

import numpy as np
from world.creature import Creature
from .base_agent import AgentBase

class BAgent(AgentBase):
    """Agent moving towards best grass in range"""

    COLOR = (5, 150, 5)
    IS_PREDATOR = True
    OWN_POS = 0, 0

    def __init__(self, world, creature):
        self.vision_range = 1
        self.grass = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        self.walkable = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        super(BAgent, self).__init__(world, creature)
        self.creature.predator = BAgent.IS_PREDATOR
        self.vision()
        
    def step(self):
        """Runs through logic to decide next action."""
        action = self.logic()
        valid = self.creature.request_action(action)
        assert valid, 'Invalid action!'

    def logic(self):
        """Decides what action to take next"""
        #self.vision()
        grass_pos = np.unravel_index(np.argmax(self.grass), shape=self.grass.shape)
        grass_pos = grass_pos[0] - self.vision_range, grass_pos[1] - self.vision_range

        if self.creature.get_food() > 0.95:
            return Creature.REPRODUCE
        if self.creature.get_food() <= 0.1 or (0.50 > self.creature.get_food() > 0.45):
            if random.randint(6, 9) == 7:
                return Creature.WALK
            return Creature.EAT
        if random.randint(0,16) == 7:
            return Creature.TURN_R
        if random.randint(0,17) == 7:
            return Creature.TURN_L
        if random.randint(6, 9) == 7:
            return Creature.WALK
        if self.creature.get_food() > 0.25 and self.creature.get_food() < 0.35 and random.randint(0,2) == 1:
            return Creature.KILL
        if self.creature.get_food() < 0.95:
            return Creature.EAT


        grass_direction = self.best_direction(grass_pos)
        return self.move(grass_direction)

    def move(self, direction):
        """Move in given direction if facing the right way, else turn towards that direction"""
        if self.creature.d == direction:
            return Creature.WALK
        if self.creature.d - direction == 1:
            return Creature.TURN_L
        return Creature.TURN_R

    @staticmethod
    def best_direction(pos):
        """Find best direction to walk given destination in relative position (i, j)"""
        if abs(pos[0]) >= abs(pos[1]):
            if pos[0] < 0:
                return Creature.W
            return Creature.E
        if pos[1] < 0:
            return Creature.N
        return Creature.S

    def get_grass(self, pos):
        """Get grass value from relative position (i, j)"""
        return self.world.grass.get_value((self.creature.x + pos[0]) % self.world.grid_width,
                                          (self.creature.y + pos[1]) % self.world.grid_height)

    def is_walkable(self, pos):
        """Checks if a tile can be walked on."""
        walkable = True
        if self.world.water.is_water(self.creature.x + pos[0], self.creature.y + pos[1]):
            walkable = False
        occ = [(c.x, c.y) for c in self.world.creatures]
        if (self.creature.x + pos[0], self.creature.y + pos[1]) in occ:
            walkable = False
        return walkable

    def vision(self):
        """Finds grass in vision range, and finds walkable tiles."""
        for i in range(-self.vision_range, self.vision_range + 1):
            for j in range(-self.vision_range, self.vision_range + 1):
                self.grass[self.vision_range + i][self.vision_range + j] = self.get_grass((i, j))
                self.walkable[self.vision_range + i][self.vision_range + j] = self.is_walkable((i, j))
