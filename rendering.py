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
        #self.draw_layer(self.world.sun)
        for c in self.world.creatures:
            self.draw_creature(c)

        for x in range(self.size):
            for y in range(self.size):
                test = pygame.Surface((self.scale,self.scale))
                test.set_alpha((1-self.world.sun.grid[x][y])*30)
                self.screen.blit(test, (x*self.scale, y*self.scale))

    def draw_layer(self, layer):
        for x in range(self.size):
            for y in range(self.size):
                if layer.get_value(x, y) != 0:
                    pygame.draw.rect(self.screen, layer.get_color(layer.get_value(x, y)),
                                     (self.scale * x, self.scale * y, self.scale, self.scale))


    def draw_creature(self, c):
        (N, E, S, W) = [0, 1, 2, 3]
        rect = pygame.Rect(c.x * self.scale, c.y * self.scale, self.scale, self.scale)
        pygame.draw.rect(self.screen, c.get_color(), rect)
        if c.d == N:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale)), 3)
        elif c.d == W:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale), (c.y * self.scale) + self.scale / 2), 3)
        elif c.d == S:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale), 3)
        elif c.d == E:
            pygame.draw.line(self.screen, red,
                             ((c.x * self.scale) + self.scale / 2, (c.y * self.scale) + self.scale / 2),
                             ((c.x * self.scale) + self.scale, (c.y * self.scale) + self.scale / 2), 3)
