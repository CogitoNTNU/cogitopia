import pygame
import numpy as np
from perlin_noise import perlin_noise
from world.creature import Creature
from rendering import Renderer
from world.world import World, WorldSettings


# Grid size is the number of cells in the world
grid_size = 20 

# Scale is the pixel size of each world cell on screen
scale = 16 

pygame.init()
screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])

if __name__ == '__main__':
    # TODO: This file should only call renderer.draw_world(world, screen)
    renderer = Renderer(None, scale)
    pygame.init()
    screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])
    
    # World setup
    ws = WorldSettings()
    ws.grass_growth_rate = 5 # Example use of ws
    world = World(grid_size, ws)
    
    # TODO: Get rid of all world and creature logic, and reduce 
    # this sections to something like "while running: world.step()"

    creatures = [Creature(5, 5), Creature(7, 5), Creature(5, 10)]# belongs in world
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))
        renderer.draw_grass(world.get_grid(), screen)# belongs in renderer

        for c in creatures:
            renderer.draw_creature(c, screen)# belongs in renderer
            world.eat_grass(c.y, c.x)# belongs in world
            c.turn()# belongs in world
            c.walk()# belongs in world
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        world.step_grass()# belongs in world
        pygame.display.flip()
        clock.tick(0)
    pygame.quit()
