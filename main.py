import pygame

from world.creature import Creature
from world.world import World, WorldSettings

# Grid size is the number of cells in the world
size = 20

# Scale is the pixel size of each world cell on screen
scale = 16
screen = pygame.display.set_mode([size * scale, size * scale])

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    world = World(size, scale)
    world.add_creature(Creature(5, 5, size, world))
    world.add_creature(Creature(7, 5, size, world))
    world.add_creature(Creature(5, 10, size, world))

    # World setup
    ws = WorldSettings()
    ws.grass_growth_rate = 5  # Example use of ws

    agents = []

    running = True

    while running:
        # Process input
        screen.fill((0, 100, 0))
        world.draw_world()

        for c in world.creatures:
            c.turn()
            c.walk()
            world.grass.eat_grass(c.x, c.y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step agents
        for agent in agents:
            agent.step()

        # Step world
        world.update()

        # Render everything and display
        # screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(0)

    pygame.quit()
