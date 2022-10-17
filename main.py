import pygame

from world.creature import Creature
from world.world import World

pygame.init()
grid_size = 20
scale = 32
screen = pygame.display.set_mode([grid_size * scale, grid_size * scale])

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    world = World(grid_size, scale)
    world.add_creature(Creature(5, 5))
    world.add_creature(Creature(7, 5))
    world.add_creature(Creature(5, 10))

    running = True
    while running:
        screen.fill((0, 100, 0))
        world.draw_world()
        world.update()

        for c in world.creatures:
            c.turn()
            c.walk()
            world.grass.eat_grass(c.x, c.y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(9)
    pygame.quit()
