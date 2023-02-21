"""
Module representing the world.
"""
from random import randint
import numpy as np
from perlin_noise import PerlinNoise
import yaml

from .world import World
from world.world import WorldSettings as WorldSettings
from .creature import Creature
from train import TrainAgent

#import random
#import sys
#from collections import deque
from gym import spaces
import gym
#import itertools

# WorldSettings should have all constants that
# are related to the simulation (not rendering)



# Variables that change during simulation, such
# as time, belongs in the World class

class TrainWorld(gym.Env):
    def __init__(self):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), False)
        self.player = TrainAgent(self, self.creature)
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,self.world.grid_width,self.world.grid_height), dtype=np.uint8)

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self, color, predator)
        self.creatures.append(creature)
        self.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def step(self):
        state = self.init_state()
        reward = 0
        done = False
        info = {}

        self.world.step()

        survive = self.player.tick()
        if self.player.action == Creature.REPRODUCE:
            reward = 1

        # Death

        survive = self.player.tick()
        if not survive:
            reward = -1
            done = True

        return state, reward, done, info
