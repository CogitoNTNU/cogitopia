"""
Module representing the world.
"""
import numpy as np


from world.world import World
from world.world import WorldSettings as WorldSettings
from world.creature import Creature
from agents.train import TrainAgent
from gym import spaces
import gym

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

        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
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
        self.player = TrainAgent(self.world, self.creature)
        self.world_age = 1
        self.agents = []
        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
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
            self.agents[i].step()
        self.player.step()
        self.world.step()
        survive = self.player.tick()
        self.world_age += 1



        # Death
        reward += len(list(filter(lambda x: not x.creature.predator, self.agents))) + self.player.creature.food-0.3
        survive = self.player.tick()
        self.player.vision()
        state = [np.stack((np.array(self.player.grass), np.array(self.player.walkable), np.array(self.player.other_creatures), np.array(self.player.other_dead_creatures), np.ones((self.player.vision_range*2+1, self.player.vision_range*2+1))*food_0))]
        for agent in self.agents:
            agent.vision()
            reward += agent.creature.food-0.3
            agentstate = [np.stack((np.array(agent.grass), np.array(agent.walkable),
                               np.array(agent.other_creatures), np.array(agent.other_dead_creatures),
                               np.ones((agent.vision_range * 2 + 1, agent.vision_range * 2 + 1)) * food_0))]

            state.append(np.stack(agentstate))
        if not survive:
            reward = (-1000 + self.world_age/3)*0.1
            done = True
        done = done or len(list(filter(lambda x: not x.creature.predator, self.agents))) > 2048 or self.world_age > 3000
        return state, reward, done, info

