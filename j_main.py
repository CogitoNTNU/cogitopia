import random
import gym
import time
import git
import pygame
import wandb

from agents.t_agent import TAgent
from agents.j_agent import JAgent
from agents.b_agent import BAgent
from agents.sau_agent import SauAgent
from rendering import Renderer
from world.world import World, WorldSettings

if __name__ == '__main__':
    ws = WorldSettings()

from stable_baselines3 import PPO
from stable_baselines3.common.logger import configure
from stable_baselines3.common.env_util import make_vec_env
from agents.train import TrainAgent
from train_world import TrainWorld

# Grid size is the number of cells in the world
grid_width, grid_height = (ws.grid_width, ws.grid_height)

# Scale is the pixel size of each world cell on screen
scale = ws.scale

pygame.init()
screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])
clock = pygame.time.Clock()

# World setup
world = World(grid_width, grid_height, ws)
renderer = Renderer(world, scale, screen)

agents = []

def spawn(amount, agent_type):
    for _ in range(amount):
        x_pos = random.randrange(grid_width)
        y_pos = random.randrange(grid_height)
        if world.water.get_value(x_pos, y_pos) == 0:
            creature = world.spawn_creature(x_pos, y_pos, agent_type.COLOR, agent_type.IS_PREDATOR)
            agents.append(agent_type(world, creature))

def reproduction_callback(parent):
    c = world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
    agents.append(parent.agent_type(world, c))

world.reproduction_callback = reproduction_callback

running = True

spawn(100, JAgent)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Step agents
    for agent in agents:
        if agent.world.is_dead(agent.creature):
            agents.remove(agent)
        else:
            agent.step()
    
    # Step world
    world.step()

    # Render everything and display
    screen.fill((0, 0, 0))
    renderer.draw_world()
    pygame.display.flip()

    clock.tick(0)

pygame.quit()
