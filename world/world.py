"""
Module representing the world.
"""
from random import randint
import numpy as np
from perlin_noise import PerlinNoise
import yaml

from .earth import Earth
from .grass import Grass
from .temperature import Temperature
from .height import Height
from .water import Water
from .sun import Sun
from .creature import Creature
from .smell import Smell


# WorldSettings should have all constants that
# are related to the simulation (not rendering)

class WorldSettings:
    """Global settings."""
    with open("Settings.yml", "r") as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    use_temp = settings["use_temp"]
    grass_growth_rate = settings["grass_growth_rate"]
    scale = settings["scale"]
    grid_width = settings["grid_width"]
    grid_height = settings["grid_height"]
    t_agent_amount = settings["t_agent_amount"]
    j_agent_amount = settings["j_agent_amount"]
    b_agent_amount = settings["b_agent_amount"]
    clock_speed = settings["clock_speed"]
    creature_starting_food = settings["creature_starting_food"]
    turning_food_cost = settings["turning_food_cost"]
    walking_food_cost = settings["walking_food_cost"]
    walking_in_water_cost = settings["walking_in_water_cost"]
    reproduction_cost = settings["reproduction_cost"]
    killing_cost = settings["killing_cost"]


# Variables that change during simulation, such
# as time, belongs in the World class

class World:
    def __init__(self, grid_width, grid_height, settings):
        self.settings = settings
        self.time = 0
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grass = Grass(self.grid_width, self.grid_height, self.initialize(), self)
        self.earth = Earth(self.grid_width, self.grid_height, self.initialize(), self)
        self.smell = Smell(self.grid_width, self.grid_height, self.initialize(1), self)
        self.temperature = Temperature(self.grid_width, self.grid_height, self.initialize(), self)
        self.height = Height(self.grid_width, self.grid_height, self.initialize(1), self)
        self.water = Water(self.grid_width, self.grid_height, self.height, self)
        self.sun = Sun(self.grid_width, self.grid_height, self)
        self.creatures = []
        self.reproduction_callback = lambda: None
        self.creatures_array = [[[] for _ in range(self.grid_height)] for _ in range(self.grid_width)]
        self.murders = 0

    def spawn_creature(self, x_pos, y_pos, color, predator):
        creature = Creature(x_pos, y_pos, self, color, predator)
        self.creatures.append(creature)
        self.creatures_array[x_pos][y_pos].append(creature)
        return creature

    def step(self):
        for creature in self.creatures:
            creature.process_action()
            #if creature.is_dead and creature.meat < 0:
                #self.creatures.remove(creature)
                #self.creatures_array.remove(creature)

        self.grass.step()
        self.earth.step()
        self.smell.step()
        if self.settings.use_temp:
            self.temperature.step()
        self.sun.step(self.time)
        self.inc_time()

    def initialize(self, octaves=5):
        noise = PerlinNoise(octaves=octaves, seed=randint(1, 20))
        pic = [[abs(noise([i / self.grid_width, j / self.grid_height])) for j in range(self.grid_height)] for i in
               range(self.grid_width)]
        return pic

    def get_time(self):
        return self.time

    def inc_time(self):
        self.time += 1

    @staticmethod
    def is_dead(creature):
        if creature.get_food() <= 0:
            creature.is_dead = True
        return creature.is_dead

    def get_creatures_at_location(self, x, y):
        return self.creatures_array[x][y]
