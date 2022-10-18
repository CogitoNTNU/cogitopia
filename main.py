import pygame

from world.creature import Creature
from world.world import World
import numpy as np
from perlin_noise import perlin_noise
from rendering import Renderer
from world.world import World, WorldSettings
from agent import Agent

# Grid size is the number of cells in the world
grid_size = 20

# Scale is the pixel size of each world cell on screen
scale = 16
screen = pygame.display.set_mode([size * scale, size * scale])

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    world = World(size, scale)
    world.add_creature(Creature(5, 5, size))
    world.add_creature(Creature(7, 5, size))
    world.add_creature(Creature(5, 10, size))


    # World setup
    ws = WorldSettings()
    ws.grass_growth_rate = 5 # Example use of ws

    world = World(grid_size, ws)
    renderer = Renderer(world, scale, screen)
    agents = []
    for i in range(5):
        c = world.spawn_creature(5, 5)
        agents.append(Agent(world, c))

    running = True

    while running:
        # Process input
        screen.fill((0, 100, 0))
        world.draw_world()
        world.update()

        for c in world.creatures:
            c.turn()
            c.walk()
            world.grass.eat_grass(c.x, c.y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Step agents
        for agent in agents:
            agent.step()

        # Step world
        world.step()

        # Render everything and display
        screen.fill((0, 0, 0))
        renderer.draw_world()
        pygame.display.flip()
        clock.tick(0)

    pygame.quit()
