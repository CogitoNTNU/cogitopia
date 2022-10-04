import pygame
from random import randrange
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise
from renderng import rendering
from world import world
from creature import Creature
pygame.init()

screen = pygame.display.set_mode([800, 800])

world = world(20)
c=Creature(5,5,1)
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 150, 0))
    rendering.draw_grass(world.get_grid(),screen)
    #rendering.draw_earth(world.get_grid(),screen)
    #rendering.draw_height(world.get_grid(),screen)
    #rendering.draw_water(world.get_grid(),screen)
    rendering.draw_creature(c,screen)
    world.step_grass()
    #world.step_water()

        #rendering.draw_player(grid,screen)
        #rendering.draw_earth(grid,screen)
    pygame.display.flip()


pygame.quit()