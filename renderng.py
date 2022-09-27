
import numpy as np
import pygame
layer_dict = {'grass' : 0, 'earth' : 1, 'water' : 2 ,'player' : 10}

class rendering:
    def draw_grass(grid,screen):
            for y in range(len(grid[0])):
                for x in range(len(grid[0][0])):
                        pygame.draw.rect(screen, (0, grid[layer_dict['grass']][y][x]* 180 + 75, 0), (50*x, 50*y, 50, 50))
    def draw_player(grid,screen):
            for y in range(len(grid[0])):
                for x in range(len(grid[0][0])):
                    if grid[layer_dict['player']][y][x] != None:
                        pygame.draw.circle(screen, (grid[layer_dict['player']][y][x],0, 0), (50 * x-25, 50 * y+25),20)
    def draw_earth(grid,screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(screen, (grid[layer_dict['earth']][y][x]* 180 + 75, grid[layer_dict['earth']][y][x]*0.6* 180 + 75, 0), (50 * x, 50 * y, 50, 50))
    def draw_water(grid,screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(screen, (0,0,grid[layer_dict['earth']][y][x]), (50 * x, 50 * y, 50, 50))


    


