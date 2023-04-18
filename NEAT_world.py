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
    def __init__(self, genome_counts):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = [self.world.spawn_creature(np.random.randint(0, 40), np.random.randint(0, 20), (5, 150, 5), False) for i in range(genome_counts)]
        self.players = [TrainAgent(self.world, self.creature[i], i) for i in range(genome_counts)]
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, self.players[0].vision_range*2+1, self.players[0].vision_range*2+1))
        self.world_age = 1
        self.callback = None
        self.agents = [[]]*genome_counts

        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents[parent.i].append(parent.agent_type(self.world, c, parent.i))
            return True
        self.world.reproduction_callback = reproduction_callback

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self.world, color, predator)
        self.world.creatures.append(creature)
        self.world.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def init_state(self):
        return np.zeros(shape=(5, self.players[0].vision_range*2+1, self.players[0].vision_range*2+1))

    def reset(self):
        self.world = World(grid_width=40, grid_height=20, settings=WorldSettings())
        self.creature = [self.world.spawn_creature(np.random.randint(0, 40), np.random.randint(0, 20), (5, 150, 5), False)]*len(self.players)
        self.players = [TrainAgent(self.world, self.creature[i], i) for i in range(len(self.creature))]
        self.world_age = 1
        self.agents = [[]]*len(self.players)
        def reproduction_callback(parent):
            c = self.world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
            self.agents.append(parent.agent_type(self.world, c))
            return True
        self.world.reproduction_callback = reproduction_callback
        return self.init_state()

    def step(self, action):
        food_0 = [creature.food for creature in self.creature]
        reward = [0]*len(self.players)
        state = [[]]*len(self.players)
        done = [False]*len(self.players)
        info = {}
        if type(action) != list:
            if type(action[0]) != list:
                action = [list(ac) for ac in action]
            else:
                action = list(action)
        for i in range(len(action)):
            self.players[i].action = action[i][0]
            for j in range(min(len(action)-1, len(self.agents[i]))):
                self.agents[i][j].action = action[i][j+1]
                self.agents[i][j].step()
            self.players[i].step()
        self.world.step()
        self.world_age += 1



        # Death
        for i in range(len(self.players)):
            survive = self.players[i].tick()
            reward[i] += len(list(self.agents[i])) + self.players[i].creature.food-0.3
            survive = self.players[i].tick()
            self.players[i].vision()
            state[i] = [np.stack((np.array(self.players[i].grass), np.array(self.players[i].walkable), np.array(self.players[i].other_creatures), np.array(self.players[i].other_dead_creatures), np.ones((self.players[i].vision_range*2+1, self.players[i].vision_range*2+1))*self.players[i].creature.food))]
            for agent in self.agents[i]:
                agent.vision()
                reward[i] += agent.creature.food-0.3
                agentstate = [np.stack((np.array(agent.grass), np.array(agent.walkable),
                                   np.array(agent.other_creatures), np.array(agent.other_dead_creatures),
                                   np.ones((agent.vision_range * 2 + 1, agent.vision_range * 2 + 1)) * agent.creatue.food))]

                state[i].append(np.stack(agentstate))
            if not survive:
                reward[i] = (-1000 + self.world_age/3)*0.1
                done[i] = True
        done = np.all(done) or len(list(filter(lambda x: not x.predator, self.world.creatures))) > 3072 or self.world_age > 3000
        return state, reward, done, info

