import random

import pygame

from agent import Agent
from t_agent import TAgent
from j_agent import JAgent
from rendering import Renderer
from world.world import World, WorldSettings


# Grid size is the number of cells in the world
grid_width, grid_height = (40, 20)

# Scale is the pixel size of each world cell on screen
scale = 32

pygame.init()
screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])
    clock = pygame.time.Clock()

    # World setup
    ws = WorldSettings()
    ws.use_temp = False
    ws.grass_growth_rate = 1# Example use of ws

    world = World(grid_width, grid_height, ws)
    renderer = Renderer(world, scale, screen)
    agents = []

    while len(agents) < 1:
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (0, 0, 0))
            agents.append(Agent(world, c))

    while len(agents) < 2:
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (50, 50, 50))
            agents.append(TAgent(world, c))

    while len(agents) < 3:
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (100, 50, 50))
            agents.append(JAgent(world, c))

    def reproduction_callback(parent):
        c = world.spawn_creature(parent.x, parent.y, parent.color)
        agents.append(parent.agent_type(world, c))

    world.reproduction_callback = reproduction_callback

    running = True

    while running:
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step agents
        for agent in agents:
            if agent.world.is_dead(agent.creature):
                #agent.creature.remove_from_array()
                #agents.remove(agent)
                #world.creatures.remove(agent.creature)
                pass
            else:
                agent.step()
        # Step world
        world.step()

        # Render everything and display
        screen.fill((0, 0, 0))
        renderer.draw_world()
        pygame.display.flip()
        clock.tick(100)
        clock.tick(0)

    pygame.quit()
