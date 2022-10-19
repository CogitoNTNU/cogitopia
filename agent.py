from world.creature import Creature
import numpy as np


class Agent:
    def __init__(self, world, creature):
        self.world = world
        self.creature = creature

    def step(self):
        valid = False
        while not valid:
            action = np.random.choice([Creature.EAT, Creature.TURN_L, Creature.TURN_R, Creature.WALK])
            valid = self.creature.request_action(action)
