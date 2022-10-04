import pygame
import numpy as np
from random import randrange
import random
grid_size=20
(N,W,S,E)=[0,1,2,3]
class Creature:
    def __init__(self,x,y,d):
        self.x=x
        self.y=y
        self.d=randrange(3)
    def step(self):
            if self.d==N:
                self.d=random.choice((N,W,E)) #bestemmer ny retning
                if self.d==N:
                    self.y=(self.y+1)%grid_size
            elif self.d==W:
                self.d=random.choice((N,W,S))
                if self.d==W:
                    self.x=(self.x+1)%grid_size
            elif self.d==S:
                self.d=random.choice((S,W,E))
                if self.d==S:
                    self.y=(self.y-1)%grid_size
            elif self.d==E:
                self.d=random.choice((E,N,S))
                if self.d==E:
                    self.x=(self.x-1)%grid_size