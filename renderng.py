
import numpy as np
import pygame
layer_dict = {'grass' : 0, 'earth' : 1, 'water' : 2 ,'player' : 10,'temperature':3,'heigh':4}
cell_size=32
black = (0, 0, 0)
white = (200, 200, 200)
red=(255,0,0)
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
                if grid[layer_dict['water']][y][x] != 0:
                    pygame.draw.rect(screen, (0,0,grid[layer_dict['water']][y][x]*50+50), (50 * x, 50 * y, 50, 50))
    def draw_temp(grid,screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(screen, (grid[layer_dict['temperature']][y][x]*100+50,0,0), (50 * x, 50 * y, 50, 50))
    def draw_height(grid,screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(screen, (grid[layer_dict['heigh']][y][x]*200,grid[layer_dict['heigh']][y][x]*200,grid[layer_dict['heigh']][y][x]*200), (50 * x, 50 * y, 50, 50))
    def draw_creature(c, screen):
        (N,W,S,E)=[0,1,2,3]
        rect = pygame.Rect(c.x*cell_size, c.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, black, rect)
        if c.d==S:
            pygame.draw.line(screen, red, ((c.x*cell_size)+cell_size/2,(c.y*cell_size)+cell_size/2), ((c.x*cell_size)+cell_size/2,(c.y*cell_size)),3)
        elif c.d==E:
            pygame.draw.line(screen, red, ((c.x*cell_size)+cell_size/2,(c.y*cell_size)+cell_size/2), ((c.x*cell_size),(c.y*cell_size)+cell_size/2),3)
        elif c.d==N:
            pygame.draw.line(screen, red, ((c.x*cell_size)+cell_size/2,(c.y*cell_size)+cell_size/2), ((c.x*cell_size)+cell_size/2,(c.y*cell_size)+cell_size),3)
        elif c.d==W:
            pygame.draw.line(screen, red, ((c.x*cell_size)+cell_size/2,(c.y*cell_size)+cell_size/2), ((c.x*cell_size)+cell_size,(c.y*cell_size)+cell_size/2),3)   


    


