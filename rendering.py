import pygame
import scipy
import numpy as np
import world.world

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
        self.font = pygame.font.SysFont('Arial',25)

    def draw_world(self):
        self.draw_layer(self.world.earth)
        self.draw_layer(self.world.grass)
        self.draw_layer(self.world.water)
        self.draw_layer(self.world.clouds)
        #self.draw_layer(self.world.ice)
        #self.draw_flower(self.world.flowers)
        #self.draw_layer(self.world.temperature)
        #self.draw_layer(self.world.height)
        #self.draw_layer(self.world.moveableWater)
        self.draw_sun()
        if world.world.WorldSettings.show_value != "":
            self.draw_text(world.world.WorldSettings.show_value)
        #self.draw_height()
        #self.draw_layer(self.world.smell)
        for c in self.world.creatures:
            self.draw_creature(c)

        self.draw_hud()


    def draw_layer(self, layer):
        #grid = layer.grid
        #grid = scipy.ndimage.convolve(layer.grid, [[0.25, 0.25], [0.25, 0.25]])
        #grid = scipy.ndimage.convolve(layer.grid,[[0, 0., 0], [0., 1, 0.], [0.0, 0.0, 0.0]])
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if layer.get_value(x, y) != 0:
                    pygame.draw.rect(self.screen, layer.get_color(layer.get_value(x, y)),(self.scale * x, self.scale * y, self.scale, self.scale))
                    #pygame.draw.rect(self.screen, layer.get_color(grid[x, y]),
                                     #(self.scale * x, self.scale * y, self.scale, self.scale))
    def draw_sun(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                test = pygame.Surface((self.scale,self.scale))
                test.set_alpha((1-self.world.sun.grid[x][y])*100*(self.world.height.grid[x][y]))
                self.screen.blit(test, (x*self.scale, y*self.scale))
    def draw_flower(self,layer):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if layer.get_value(x, y) != 0:
                    offsets = np.array([[-0.2,0.8],[-0.8,0.2],[-0.8,0.8],[-0.2,0.2],[-0.5,0.5]])
                    for i in range(int(layer.get_value(x,y)*5)):
                        x_offset = offsets[i,0]
                        y_offset = offsets[i,1]

                        pygame.draw.circle(self.screen,layer.get_color(layer.get_value(x,y)),(self.scale * (x-x_offset), self.scale * (y-y_offset+1)),radius=self.scale*0.2)
                        pygame.draw.circle(self.screen, layer.get_second_color(layer.get_value(x, y)),
                                           (self.scale * (x-(x_offset)), self.scale * (y-y_offset+1)), radius=self.scale * 0.1)

                    # pygame.draw.circle(self.screen, layer.get_color(layer.get_value(x, y)),
                    #                    (self.scale * (x-0.5), self.scale * (y-0.5)), radius=self.scale * 0.2)
                    # pygame.draw.circle(self.screen, layer.get_second_color(layer.get_value(x, y)),
                    #                    (self.scale * (x-0.5), self.scale * (y-0.5)), radius=self.scale * 0.1)
                    # pygame.draw.circle(self.screen, layer.get_color(layer.get_value(x, y)),
                    #                    (self.scale * (x-np.random.random()), self.scale * (y-np.random.random())), radius=self.scale * 0.2)
                    # pygame.draw.circle(self.screen, layer.get_second_color(layer.get_value(x, y)),
                    #                    (self.scale * (x-np.random.random()), self.scale * (y-np.random.random())), radius=self.scale * 0.1)

    def draw_height(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                test = pygame.Surface((self.scale, self.scale))
                test.set_alpha( 244 * (self.world.height.grid[x][y]))
                self.screen.blit(test, (x * self.scale, y * self.scale))
    def draw_text(self,type):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                test = pygame.Surface((self.scale,self.scale))
                if type == 'height':
                    self.screen.blit(self.font.render(str(round(self.world.height.grid[x][y]*100)),True,(255,0,0)),(x * self.scale, y * self.scale))
                elif type == 'grass':
                    self.screen.blit(self.font.render(str(round(self.world.grass.grid[x][y]*100)),True,(255,0,0)),(x * self.scale, y * self.scale))
                elif type == 'temperature':
                    self.screen.blit(self.font.render(str(round(self.world.temperature.grid[x][y]*100)),True,(255,0,0)),(x * self.scale, y * self.scale))
                elif type == 'sun':
                    self.screen.blit(self.font.render(str(round(self.world.sun.grid[x][y]*100)),True,(255,0,0)),(x * self.scale, y * self.scale))
                elif type == 'earth':
                    self.screen.blit(self.font.render(str(round(self.world.earth.grid[x][y] * 100)), True, (255, 0, 0)),
                                     (x * self.scale, y * self.scale))



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
    