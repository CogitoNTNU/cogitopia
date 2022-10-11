import pygame
from random import randrange
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise
from rendering import rendering
from world import world
pygame.init()

screen = pygame.display.set_mode([800, 800])

world = world(20)
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 150, 0))
    rendering.draw_grass(world.get_grid(),screen)
    #rendering.draw_earth(world.get_grid(),screen)
    #rendering.draw_height(world.get_grid(),screen)
    rendering.draw_sun(world.get_grid(),screen)
    world.step_sun()
    world.step_time()

    # rendering.draw_water(world.get_grid(),screen)
    # rendering.draw_temp(world.get_grid(),screen)
    # world.step_grass()
    # #world.step_temp()
    # world.step_water()

        #rendering.draw_player(grid,screen)
        #rendering.draw_earth(grid,screen)







    pygame.display.flip()


pygame.quit()