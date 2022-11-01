import random

import pygame

from agent import Agent
from t_agent import TAgent
from j_agent import JAgent
from rendering import Renderer
from world.world import World, WorldSettings

    

# Grid size is the number of cells in the world
grid_size = 20

# Scale is the pixel size of each world cell on screen
scale = 32

pygame.init()
screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])
    clock = pygame.time.Clock()

    # World setup
    ws = WorldSettings()
    ws.grass_growth_rate = 5  # Example use of ws

    world = World(grid_size, ws)
    renderer = Renderer(world, scale, screen)
    agents = []

    while len(agents) < 1:
        x = random.randrange(grid_size)
        y = random.randrange(grid_size)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (0, 0, 0))
            agents.append(Agent(world, c))

    while len(agents) < 2:
        x = random.randrange(grid_size)
        y = random.randrange(grid_size)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (50, 50, 50))
            agents.append(TAgent(world, c))

    while len(agents) < 3:
        x = random.randrange(grid_size)
        y = random.randrange(grid_size)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (100, 50, 50))
            agents.append(JAgent(world, c))
    
    def reproduction_callback(parent):
        c = world.spawn_creature(x, y, (100, 50, 50))
        agents.append(parent.agent_type(world, c))
        
    world.reproduction_callback = reproduction_callback

    running = True

    while running:
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            while event.type == pygame.KEYDOWN:
                pass

        # Step agents
        for agent in agents:
            if agent.world.is_dead(agent.creature):
                agents.remove(agent)
                world.creatures.remove(agent.creature)
            else:
                agent.step()
        # Step world
        world.step()

        # Render everything and display
        screen.fill((0, 0, 0))
        renderer.draw_world()
        renderer
        pygame.display.flip()
        clock.tick(0)

    pygame.quit()
