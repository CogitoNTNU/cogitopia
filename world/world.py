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
    grass_growth_rate = 10


# Variables that change during simulation, such
# as time, belongs in the World class

class World:
    def __init__(self, size, ws):
        self.ws = ws
        self.time = 0
        self.size = size
        self.grass = Grass(self.size, self.initialize(), self)
        self.earth = Earth(self.size, self.initialize(), self)
        self.temperature = Temperature(self.size, self.initialize(), self)
        self.height = Height(self.size, self.initialize(1), self)
        self.water = Water(self.size, self.height, self)
        self.sun = Sun(self.size, self)
        self.creatures = []

    def spawn_creature(self, x, y):
        creature = Creature(x, y, self)
        self.creatures.append(creature)
        return creature

    def step(self):
        for c in self.creatures:
            c.process_action()

        self.grass.step()
        self.earth.step()
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
            print("Creature starved to death")
            return True
