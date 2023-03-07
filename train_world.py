"""
Module representing the world.
"""
from random import randint
import numpy as np
from perlin_noise import PerlinNoise
import yaml

from world.world import World
from world.world import WorldSettings as WorldSettings
from world.creature import Creature
from agents.train import TrainAgent

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
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=1, shape=[1])

        def reproduction_callback(parent):
            return
        self.world.reproduction_callback = reproduction_callback

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self, color, predator)
        self.world.creatures.append(creature)
        self.world.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def init_state(self):
        return np.array([self.creature.food])

    def reset(self):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), False)
        self.player = TrainAgent(self, self.creature)
        def reproduction_callback(parent):
            return
        self.world.reproduction_callback = reproduction_callback
        return self.init_state()

    def step(self, action):
        state = np.array([self.creature.food])
        reward = 0
        done = False
        info = {}
        self.player.action = action
        self.player.step()
        self.world.step()
        survive = self.player.tick()
        if self.player.action == Creature.REPRODUCE:
            reward = 1

        # Death
        reward += self.creature.food - state[0]
        survive = self.player.tick()
        if not survive:
            reward = -1
            done = True

        return state, reward, done, info