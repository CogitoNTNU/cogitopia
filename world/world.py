from random import randint
from perlin_noise import PerlinNoise

# WorldSettings should have all constants that
# are related to the simulation (not rendering)

from .earth import Earth
from .grass import Grass
from .temperature import Temperature
from .height import Height
from .water import Water
from .sun import Sun
from rendering import Renderer


class WorldSettings:
    grass_growth_rate = 10


# Variables that change during simulation, such
# as time, belongs in the World class

class World:
    def __init__(self, size, scale):
        self.time = 0
        self.scale = scale
        self.size = size
        self.grass = Grass(self.size, self.initialize())
        self.earth = Earth(self.size, self.initialize())
        self.temperature = Temperature(self.size, self.initialize())
        self.height = Height(self.size, self.initialize(1))
        self.water = Water(self.size, self.height)
        self.sun = Sun(self.size)
        self.renderer = Renderer(self.size, self.scale)
        self.creatures = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def update(self):
        self.grass.step(self.earth.get_layer())
        self.earth.step()
        # self.sun.step(self.time)
        # self.temperature.step()
        self.inc_time()

    def draw_world(self):
        self.renderer.draw_layer(self.grass)
        # self.renderer.draw_layer(self.earth)
        # self.renderer.draw_layer(self.temperature)
        # self.renderer.draw_layer(self.height)
        self.renderer.draw_layer(self.water)
        # self.renderer.draw_layer(self.sun)

        for c in self.creatures:
            self.renderer.draw_creature(c)

    def initialize(self, octaves=5):
        noise = PerlinNoise(octaves=octaves, seed=randint(1, 20))
        pic = [[abs(noise([i / self.size, j / self.size])) for j in range(self.size)] for i in range(self.size)]
        return pic

    def get_time(self):
        return self.time

    def inc_time(self):
        self.time += 1
