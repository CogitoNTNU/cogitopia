import pygame
import numpy as np
from perlin_noise import perlin_noise
from rendering import Renderer
from world.world import World, WorldSettings
from agent import Agent

# Grid size is the number of cells in the world
grid_size = 20

# Scale is the pixel size of each world cell on screen
scale = 16

# Framerate is the time between each tick
framerate = 0

pygame.init()
screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])
    clock = pygame.time.Clock()
    
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
        clock.tick(framerate)

    pygame.quit()
