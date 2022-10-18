from world.creature import Creature
import numpy as np

class Agent:
    def __init__(self, world, creature):
        self.world = world
        self.creature = creature

    def step(self):
        action = np.random.choice([Creature.EAT, Creature.TURN_L, Creature.WALK])
        self.creature.request_action(action)
