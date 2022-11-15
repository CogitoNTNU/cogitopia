"""Torgeirs (stupid) agent"""
import numpy as np
from world.creature import Creature
from base_agent import AgentBase


class TAgent(AgentBase):
    """Agent moving towards best grass in range"""

    OWN_POS = 0, 0

    def __init__(self, world, creature):
        self.vision_range = 4
        self.grass = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        self.walkable = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        self.other_creatures = [[[] for _ in range(self.vision_range * 2 +1)] for _ in range(self.vision_range * 2 + 1)]
        super(TAgent, self).__init__(world, creature)

    def step(self):
        """Runs through logic to decide next action."""
        action = self.logic()
        valid = self.creature.request_action(action)
        assert valid, 'Invalid action!'

    def logic(self):
        """Decides what action to take next"""
        self.vision()
        grass_pos = np.unravel_index(np.argmax(self.grass), shape=self.grass.shape)
        grass_pos = grass_pos[0] - self.vision_range, grass_pos[1] - self.vision_range

        if self.creature.get_food() > 0.8:
            return Creature.REPRODUCE

        if self.creature.get_food() < 1.3 and self.get_grass(self.OWN_POS) > 0.05:
            return Creature.EAT

        if grass_pos == self.OWN_POS:
            return Creature.STAY

        if len(self.world.get_creatures_at_location(self.creature.x, self.creature.y)) > 1:
            return Creature.KILL

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
        return walkable

    def get_creatures(self, pos):
        """Gets creatures in vision range"""
        x_pos = (self.creature.x + pos[0]) % self.world.grid_width
        y_pos = (self.creature.y + pos[1]) % self.world.grid_height
        return self.world.creatures_array[x_pos][y_pos]

    def vision(self):
        """Finds grass in vision range, and finds walkable tiles."""
        for i in range(-self.vision_range, self.vision_range + 1):
            for j in range(-self.vision_range, self.vision_range + 1):
                self.grass[self.vision_range + i][self.vision_range + j] = self.get_grass((i, j))
                self.walkable[self.vision_range + i][self.vision_range + j] = self.is_walkable((i, j))
                self.other_creatures[self.vision_range + i][self.vision_range + j] = self.get_creatures((i, j))
