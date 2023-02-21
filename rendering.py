import pygame

black = (0, 0, 0)
white = (200, 200, 200)
red = (255, 0, 0)


class Renderer:
    def __init__(self, world, scale, screen):
        self.scale = scale
        self.world = world
        self.screen = screen
        self.grid_width = world.grid_width
        self.grid_height = world.grid_height

    def draw_world(self):
        self.draw_layer(self.world.grass)
        self.draw_layer(self.world.water)
        self.draw_sun()
<<<<<<< HEAD
        
=======
>>>>>>> 65862a9501016222983a7b9e42f31afc3ad0d218
        for c in self.world.creatures:
            self.draw_creature(c)

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                test = pygame.Surface((self.scale,self.scale))
                test.set_alpha((1-self.world.sun.grid[x][y])*30)
                self.screen.blit(test, (x*self.scale, y*self.scale))
        self.draw_hud()

    def draw_layer(self, layer):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if layer.get_value(x, y) != 0:
                    pygame.draw.rect(self.screen, layer.get_color(layer.get_value(x, y)),
                                     (self.scale * x, self.scale * y, self.scale, self.scale))
    def draw_sun(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                test = pygame.Surface((self.scale,self.scale))
                test.set_alpha((1-self.world.sun.grid[x][y])*30)
                self.screen.blit(test, (x*self.scale, y*self.scale))

    def draw_creature(self, c):
        (N, E, S, W) = [0, 1, 2, 3]
        rect = pygame.Rect(c.x * self.scale, c.y * self.scale, self.scale, self.scale)
        pygame.draw.rect(self.screen, c.get_color() if not c.is_dead else (1.,1.,1.,1.), rect)
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
    
    def draw_hud(self):
        texts = [
            'Creatures total: {}'.format(len(self.world.creatures)),
            'Creatures alive: {}'.format(len(list(filter(lambda x: not x.is_dead,self.world.creatures)))),
            'World time: {}'.format(self.world.time)
        ]

        for i, text in enumerate(texts):
            font = pygame.font.SysFont(None, 24)
            img = font.render(text, True, (255, 255, 255))
            self.screen.blit(img, (16, 16 + i * 24))
    