"""
Module representing the world.
"""
from random import randint
from perlin_noise import PerlinNoise

from .earth import Earth
from .grass import Grass
from .temperature import Temperature
from .height import Height
from .water import Water
from .sun import Sun
from .creature import Creature


# WorldSettings should have all constants that
# are related to the simulation (not rendering)

class WorldSettings:
    """Global settings."""
    grass_growth_rate = 0.2


# Variables that change during simulation, such
# as time, belongs in the World class

class World:
    def __init__(self, size, settings):
        self.settings = settings
        self.time = 0
        self.size = size
        self.grass = Grass(self.size, self.initialize(), self)
        self.earth = Earth(self.size, self.initialize(), self)
        self.temperature = Temperature(self.size, self.initialize(), self)
        self.height = Height(self.size, self.initialize(1), self)
        self.water = Water(self.size, self.height, self)
        self.sun = Sun(self.size, self)
        self.creatures = []
        self.reproduction_callback = lambda : None

    def spawn_creature(self, x_pos, y_pos, color):
        creature = Creature(x_pos, y_pos, self, color)
        self.creatures.append(creature)
        return creature

    def step(self):
        for creature in self.creatures:
            creature.process_action()

        self.grass.step()
        self.earth.step()
        self.temperature.step()
        self.sun.step(self.time)
        self.inc_time()

    def initialize(self, octaves=5):
        noise = PerlinNoise(octaves=octaves, seed=randint(1, 20))
        pic = [[abs(noise([i / self.size, j / self.size])) for j in range(self.size)] for i in range(self.size)]
        return pic

    def get_time(self):
        return self.time

    def inc_time(self):
        self.time += 1

    @staticmethod
    def is_dead(creature):
        if creature.get_food() <= 0:
            print("Creature {} starved to death".format(creature.id))
            return True
        elif creature.get_inf_loop():
            print("Creature {} got stuck in an infinite loop and died".format(creature.id))
            return True
        return False
