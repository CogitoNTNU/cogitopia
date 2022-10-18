import pygame

black = (0, 0, 0)
white = (200, 200, 200)
red = (255, 0, 0)


class Renderer:
    def __init__(self, world, scale, screen):
        self.scale = scale
        self.world = world
        self.screen = screen
        self.size = world.size

    def draw_world(self):
        self.draw_layer(self.world.grass)        
        self.draw_layer(self.world.water)
        for c in self.world.creatures:
            self.draw_creature(c)

    def draw_layer(self, layer):
        for x in range(self.size):
            for y in range(self.size):
                if layer.get_value(x, y) != 0:
                    pygame.draw.rect(self.screen, layer.get_color(layer.get_value(x, y)),
                                     (self.scale * x, self.scale * y, self.scale, self.scale))

    def draw_creature(self, c):
        (N, E, S, W) = [0, 1, 2, 3]
        rect = pygame.Rect(c.x * self.scale, c.y * self.scale, self.scale, self.scale)
        pygame.draw.rect(self.screen, black, rect)
        if c.d == S:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale)), 3)
        elif c.d == E:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale), (c.y * self.scale) + self.scale / 2), 3)
        elif c.d == N:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale), 3)
        elif c.d == W:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale, (c.y * self.scale) + self.scale / 2), 3)
