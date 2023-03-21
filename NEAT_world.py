"""
Module representing the world.
"""
from random import randint

import git
import numpy as np
from stable_baselines3.common.vec_env import VecMonitor, SubprocVecEnv
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
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), False)
        self.player = TrainAgent(self.world, self.creature)
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, self.player.vision_range*2+1, self.player.vision_range*2+1))
        self.world_age = 1
        self.callback = None
        self.agents = []
        #self.model = PPO.load(path="ppo_agent4.zip")
        #self.predatormodel = PPO.load(path="ppo_agent4.zip")

        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
        #for i in range(25): self.agents.append(TrainAgent(self.world, self.world.spawn_creature(5, 5, (5, 150, 5), False)))
        self.world.reproduction_callback = reproduction_callback

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self.world, color, predator)
        self.world.creatures.append(creature)
        self.world.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def init_state(self):
        return np.zeros(shape=(5, self.player.vision_range*2+1, self.player.vision_range*2+1))

    def reset(self):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = self.world.spawn_creature(5, 5, (5, 150, 5), False)
        #self.predatormodel = PPO.load(path="ppo_agent4.zip")
        self.player = TrainAgent(self.world, self.creature)
        self.world_age = 1
        self.agents = []
        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
        #for i in range(25): self.agents.append(TrainAgent(self.world, self.world.spawn_creature(5, 5, (5, 150, 5), False)))
        self.world.reproduction_callback = reproduction_callback
        return self.init_state()

    def step(self, action):
        food_0 = self.creature.food
        reward = 0
        done = False
        info = {}
        if type(action) != list:
            action = list(action)
        self.player.action = action[0]
        for i in range(min(len(action)-1, len(self.agents))):
            self.agents[i].action = action[i+1]
        self.player.step()
        self.world.step()
        survive = self.player.tick()
        self.world_age += 1
        #for agent in self.agents:
            #if agent.world.is_dead(agent.creature):
            #    # agent.creature.remove_from_array()
            #    self.agents.remove(agent)
            #    # world.creatures.remove(agent.creature)
            #    continue
            #agent.vision()
            #agentstate = np.stack((np.array(agent.grass), np.array(agent.walkable),np.array(agent.other_creatures),
           #                   np.ones((agent.vision_range * 2 + 1, agent.vision_range * 2 + 1)) * agent.creature.food))

            #if agent.creature.predator:
            #    agentstate = np.stack((np.array(agent.grass), np.array(agent.walkable), np.array(agent.other_creatures), np.array(agent.other_dead_creatures),
            #                           np.ones((agent.vision_range * 2 + 1,
            #                                    agent.vision_range * 2 + 1)) * agent.creature.food))
            #    action, _states = self.predatormodel.predict(agentstate, deterministic=False)
            #else:
                #action, _states = self.model.predict(agentstate, deterministic=False)
        #    agent.action = action
        #    agent.step()



        # Death
        reward += len(list(filter(lambda x: not x.creature.predator, self.agents)))
        survive = self.player.tick()
        self.player.vision()
        state = [np.stack((np.array(self.player.grass), np.array(self.player.walkable), np.array(self.player.other_creatures), np.array(self.player.other_dead_creatures), np.ones((self.player.vision_range*2+1, self.player.vision_range*2+1))*food_0))]
        for agent in self.agents:
            agent.vision()
            agentstate = [np.stack((np.array(agent.grass), np.array(agent.walkable),
                               np.array(agent.other_creatures), np.array(agent.other_dead_creatures),
                               np.ones((agent.vision_range * 2 + 1, agent.vision_range * 2 + 1)) * food_0))]

            state.append(np.stack(agentstate))
        if not survive:
            reward = (-1000 + self.world_age/3)*0.1
            #print("dead", self.world_age, len(self.agents))
            done = True
        done = done or len(list(filter(lambda x: not x.creature.predator, self.agents))) > 2048 or self.world_age > 3000
        if(self.world_age%500 == 0):
            print(self.world_age, len(self.agents), len(list(filter(lambda x: x.creature.predator, self.agents))))
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



    env = make_vec_env(TrainWorld, n_envs=20, vec_env_cls=SubprocVecEnv)
    env = VecMonitor(env)
    # env = agent
    model = PPO("MlpPolicy", env, 1/500, batch_size=20*2048, verbose=1, tensorboard_log="./tmp/tensorlog/", n_epochs=30)
    #model.set_parameters("ppo_agent3.zip")
    wandb.tensorboard.patch(root_logdir="./tmp/tensorlog/")
    trainrun = wandb.init(project="Cogitopia ppovision",
                          entity="torghauk-team",
                          sync_tensorboard=True,
                          config={"growth_rate": ws.grass_growth_rate,
                                  "git_hash": sha,
                                  "world_settings": ws.settings})
    for i in range(0,31):
        model.learning_rate = 1/(75)
        model.learn(total_timesteps=420000, log_interval=1, progress_bar=True,
                    callback=WandbCallback(
                        gradient_save_freq=1000,
                        verbose=2,
                        log="all"
                    ))
        model.save("ppo_agent4")
    trainrun.finish()

