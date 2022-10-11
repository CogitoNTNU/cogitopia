import pygame
import numpy as np
from perlin_noise import PerlinNoise
from creature import Creature
from rendering import rendering
from world import World


pygame.init()
grid_size = 20
cell_size = 32
screen = pygame.display.set_mode([grid_size * cell_size, grid_size * cell_size])


def noise_func(size):
    noise = PerlinNoise(octaves=5, seed=10)

    x_cells, y_cells = size, size
    grid = np.zeros((2, x_cells, y_cells))
    pic = [[noise([i / x_cells, j / y_cells]) for j in range(x_cells)] for i in range(y_cells)]

    for j in range(x_cells):
        for i in range(y_cells):
            grid[0][j][i] = abs(pic[j][i]) * 180 + 75

    return grid


def draw_grid(grid):
    for layer in range(len(grid)):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                if grid[layer][y, x] != 0 and layer == 0:
                    pygame.draw.rect(screen, (0, grid[layer][y][x], 0),
                                     (cell_size * x, cell_size * y, cell_size, cell_size))
                elif grid[layer][y, x] != 0 and layer == 1:
                    pygame.draw.circle(screen, (grid[layer][y][x], 0, 0),
                                       (cell_size * x - cell_size / 2, cell_size * y + cell_size / 2), cell_size / 2)
    return grid


if __name__ == '__main__':
    pygame.init()
    grid_size = 20
    cell_size = 50
    screen = pygame.display.set_mode([grid_size * cell_size, grid_size * cell_size])
    world = World(grid_size)
    creatures = [Creature(5, 5), Creature(7, 5), Creature(5, 10)]
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 100, 0))
        rendering.draw_grass(world.get_grid(), screen)
        for c in creatures:
            rendering.draw_creature(c, screen)
            world.eat_grass(c.y, c.x)
            c.turn()
            c.walk()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        world.step_grass()
        pygame.display.flip()
        clock.tick(1)

    pygame.quit()
