"""
Module representing the world.
"""
from random import randint

import git
import numpy as np
from stable_baselines3.common.vec_env import VecMonitor
from wandb.integration.sb3 import WandbCallback

import wandb
from perlin_noise import PerlinNoise
import yaml

from world.world import World
from world.world import WorldSettings as WorldSettings
from world.creature import Creature
from agents.train import TrainAgent
from stable_baselines3 import PPO

import random
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
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), True)
        self.player = TrainAgent(self.world, self.creature)
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=1, shape=(4, self.player.vision_range*2+1, self.player.vision_range*2+1))
        self.world_age = 1
        self.callback = None
        self.agents = []
        self.model = PPO.load(path="ppo_agent2.zip")
        self.predatormodel = PPO.load(path="ppo_agent3.zip")

        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
        self.agents.append(TrainAgent(self.world, self.world.spawn_creature(5, 5, (5, 150, 5), False)))
        self.world.reproduction_callback = reproduction_callback

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self.world, color, predator)
        self.world.creatures.append(creature)
        self.world.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def init_state(self):
        return np.zeros(shape=(4, self.player.vision_range*2+1, self.player.vision_range*2+1))

    def reset(self):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), True)
        self.player = TrainAgent(self.world, self.creature)
        self.world_age = 1
        self.agents = []
        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
        self.agents.append(TrainAgent(self.world, self.world.spawn_creature(5, 5, (5, 150, 5), False)))
        self.world.reproduction_callback = reproduction_callback
        return self.init_state()

    def step(self, action):
        self.player.vision()
        food_0 = self.creature.food
        state = np.stack((np.array(self.player.grass), np.array(self.player.walkable), np.array(self.player.other_creatures), np.ones((self.player.vision_range*2+1, self.player.vision_range*2+1))*food_0))
        reward = 0
        done = False
        info = {}
        self.player.action = action
        self.player.step()
        self.world.step()
        survive = self.player.tick()
        self.world_age += 1
        for agent in self.agents:
            agent.vision()
            agentstate = np.stack((np.array(agent.grass), np.array(agent.walkable),np.array(agent.other_creatures),
                              np.ones((agent.vision_range * 2 + 1, agent.vision_range * 2 + 1)) * agent.creature.food))

            if agent.creature.predator:
                action, _states = self.predatormodel.predict(agentstate, deterministic=False)
            else:
                action, _states = self.model.predict(agentstate, deterministic=False)
            agent.action = action
            agent.step()



        # Death
        reward += self.creature.food - food_0 + len(list(filter(lambda x: not x.creature.predator, self.agents)))*0.7
        survive = self.player.tick()
        if not survive:
            reward = -1000+self.world_age
            print("dead", self.world_age, len(self.agents))
            done = True
        done = self.world_age > 1000 or done or len(self.agents) > 2000
        if(self.world_age%100 == 0):
            print(self.world_age, len(self.agents))
        return state, reward, done, info



if __name__=="__main__":
    from stable_baselines3.common.logger import configure
    from stable_baselines3.common.env_util import make_vec_env
    ws = WorldSettings()
    # Grid size is the number of cells in the world
    grid_width, grid_height = (ws.grid_width, ws.grid_height)

    # Scale is the pixel size of each world cell on screen
    scale = ws.scale

    # Get git commit hash
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    trainrun = wandb.init(project="Cogitopia ppovision",
                          entity="torghauk-team",
                          sync_tensorboard=True,
                          config={"growth_rate": ws.grass_growth_rate,
                                  "git_hash": sha,
                                  "world_settings": ws.settings})

    env = make_vec_env(TrainWorld, n_envs=2)
    env = VecMonitor(env)
    # env = agent

    model = PPO("MlpPolicy", env, 1/50000, verbose=1, tensorboard_log="./tmp/tensorlog/")
    model.set_parameters("ppo_agent3.zip")
    model.learn(total_timesteps=50000, log_interval=4,
                callback=WandbCallback(
                    gradient_save_freq=1000,
                    verbose=2,
                    log="all"
                ))
    model.save("ppo_agent3")