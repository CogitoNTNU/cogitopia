import numpy as np
import pygame

layer_dict = {'grass': 0, 'earth': 1, 'water': 2, 'player': 10, 'temperature': 3, 'heigh': 4, 'sun': 5}
black = (0, 0, 0)
white = (200, 200, 200)
red = (255, 0, 0)

class Renderer:
    def __init__(self, world, scale, screen):
        self.scale = scale
        self.world = world
        self.screen = screen

    def draw_world(self):
        self.draw_grass(self.world.get_grid())
        for c in self.world.creatures:
            self.draw_creature(c)
        
    def draw_grass(self, grid):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(self.screen, (0, grid[layer_dict['grass']][y][x] * 180 + 75, 0), (self.scale * x, self.scale * y, self.scale, self.scale))

    """
    def draw_player(self, grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                if grid[layer_dict['player']][y][x] != None:
                    pygame.draw.circle(self.screen, (grid[layer_dict['player']][y][x], 0, 0), (50 * x - 25, 50 * y + 25), 20)
    
    @staticmethod
    def draw_earth(grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(self.screen, (
                grid[layer_dict['earth']][y][x] * 180 + 75, grid[layer_dict['earth']][y][x] * 0.6 * 180 + 75, 0),
                                 (50 * x, 50 * y, 50, 50))

    @staticmethod
    def draw_water(grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                if grid[layer_dict['water']][y][x] != 0:
                    pygame.draw.rect(self.screen, (0, 0, grid[layer_dict['water']][y][x] * 50 + 50),
                                     (50 * x, 50 * y, 50, 50))

    @staticmethod
    def draw_temp(grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(self.screen, (grid[layer_dict['temperature']][y][x] * 100 + 50, 0, 0),
                                 (50 * x, 50 * y, 50, 50))

    @staticmethod
    def draw_height(grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(self.screen, (grid[layer_dict['heigh']][y][x] * 200, grid[layer_dict['heigh']][y][x] * 200,
                                          grid[layer_dict['heigh']][y][x] * 200), (50 * x, 50 * y, 50, 50))

    @staticmethod
    def draw_sun(grid, screen):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                pygame.draw.rect(self.screen, (abs((grid[layer_dict['sun']][y][x]*200)),abs(grid[layer_dict['sun']][y][x]*200),0), (50 * x, 50 * y, 50, 50))
    """

    def draw_creature(self, c):
        (N, W, S, E) = [0, 1, 2, 3]
        rect = pygame.Rect(c.x * self.scale, c.y * self.scale, self.scale, self.scale)
        pygame.draw.rect(self.screen, black, rect)
        if c.d == S:
            pygame.draw.line(self.screen, red, ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale)), 3)
        elif c.d == E:
            pygame.draw.line(self.screen, red, ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale), (c.y * self.scale) + self.scale / 2), 3)
        elif c.d == N:
            pygame.draw.line(self.screen, red, ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale), 3)
        elif c.d == W:
            pygame.draw.line(self.screen, red, ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale, (c.y * self.scale) + self.scale / 2), 3)
