import pygame
from random import randrange
import numpy as np
from numba import njit
from perlin_noise import PerlinNoise


pygame.init()

screen = pygame.display.set_mode([800, 800])

grid = np.zeros([2,10,10],dtype='i4')





def neighborPoints(N, i, j):
    neighbors = np.zeros((8, 2), dtype=np.dtype('i2'))
    neighbors[7] = [(i + 1) % N, (j - 1) % N]
    neighbors[6] = [(i - 1) % N, (j - 1) % N]
    neighbors[5] = [(i-1)%N, (j+1)%N]
    neighbors[4] = [(i+1)%N, (j+1)%N]
    neighbors[3] = [i, (j+1)%N]
    neighbors[1] = [i, (j-1)%N]
    neighbors[2] = [(i+1)%N, j]
    neighbors[0] = [(i-1)%N, j]
    return neighbors

def generate_Grid(N, M):
    grid = np.zeros((2,N, N), dtype=np.dtype('i2'))
    maxiter = 3
    it = 0
    k = 1
    while k < (M + 1) or it < maxiter:
        it += 1
        xv = randrange(N)
        yv = randrange(N)
        if grid[0][yv][xv] == 0:
            grid[0][yv][xv] = 50
            for y,x in neighborPoints(N,yv,xv):
                grid[0][y,x] = 50*2
                for y2, x2 in neighborPoints(N,y,x):
                    if grid[0][y2][x2] == 0:
                        grid[0][y2,x2] = 50*3


            k += 1
    return grid

def noise_func(gridsize):
    noise = PerlinNoise(octaves=5,seed=10)
    depth = 2

    xpix, ypix = gridsize, gridsize
    grid = np.zeros((2, xpix, ypix))
    pic = [[noise([i/xpix,j/ypix]) for j in range(xpix)] for i in range(ypix)]
    print(pic)
    for j in range(xpix):
        for i in range(ypix):
            grid[0][j][i] = abs(pic[j][i])*180+75

    return grid

#grid = generate_Grid(20,6)

grid = noise_func(20)

grid[1][4][5] = 50






def draw_grid(grid):
    for layer in range(len(grid)):
        for y in range(len(grid[0])):
            for x in range(len(grid[0][0])):
                if grid[layer][y,x] != 0 and layer == 0:
                    pygame.draw.rect(screen, (0, grid[layer][y][x], 0), (50*x, 50*y, 50, 50))
                elif grid[layer][y,x] != 0 and layer == 1:
                    pygame.draw.circle(screen, (grid[layer][y][x],0, 0), (50 * x-25, 50 * y+25),20)
    return grid

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.fill((0, 150, 0))
        grid = draw_grid(grid)






    pygame.display.flip()


pygame.quit()




