from world.creature import Creature
import numpy as np
from .base_agent import AgentBase
import gym

class Agent(AgentBase, gym.Env):
    def __init__(self, world, creature):
        super(Agent, self).__init__(world, creature)
        
    def step(self):
        valid = False
        while not valid:
            action = np.random.choice([Creature.EAT, Creature.TURN_L, Creature.TURN_R, Creature.WALK])
            valid = self.creature.request_action(action)
