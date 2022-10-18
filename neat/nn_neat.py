from rendering import Renderer
from world.world import World, WorldSettings
from world.creature import Creature

Creature.EAT()  


grid_size = 20 
ws = WorldSettings()
ws.grass_growth_rate = 5 # Example use of ws

world = World(grid_size, ws)
c = world.spawn_creature(5, 5)


def train_brain(self,c,config):
    print("Training brain")
