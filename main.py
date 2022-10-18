import pygame

from world.creature import Creature
from world.world import World

pygame.init()
size = 30
scale = 16
screen = pygame.display.set_mode([size * scale, size * scale])

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    world = World(size, scale)
    world.add_creature(Creature(5, 5, size))
    world.add_creature(Creature(7, 5, size))
    world.add_creature(Creature(5, 10, size))

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
        clock.tick(0)
    pygame.quit()
