import pygame
import numpy as np
from perlin_noise import perlin_noise
from world.creature import Creature
from rendering import Renderer
from world.world import World

pygame.init()
grid_size = 20
scale = 16
screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])

if __name__ == '__main__':
    renderer = Renderer(None, scale)
    pygame.init()
    screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])
    world = World(grid_size)
    creatures = [Creature(5, 5), Creature(7, 5), Creature(5, 10)]
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 100, 0))
        renderer.draw_grass(world.get_grid(), screen)
        for c in creatures:
            renderer.draw_creature(c, screen)
            world.eat_grass(c.y, c.x)
            c.turn()
            c.walk()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        world.step_grass()
        pygame.display.flip()
        clock.tick(0)
    pygame.quit()
