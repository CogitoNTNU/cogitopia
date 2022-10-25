from world.creature import Creature
import numpy as np

class AgentLocalMax:
  def __init__(self, world, creature):
    self.world = world
    self.creature = creature
    vision_size = 2
    self.grid_size = self.world.grid_size
  
  def acquire_target(self):
    x = self.creature.x
    y = self.creature.y
    for i in range((-vision_size + x) % self.grid_size , (vision_size + x) % self.grid_size):
      for j in range((-vision_size + y) % self.grid_size , (vision_size + y) % self.grid_size):
        get info on local area and eat
  
  def step(self):
    self.creature.request_action(action)
