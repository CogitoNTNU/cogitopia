"""An experimental training facade"""
import numpy as np
from world.creature import Creature
from base_agent import AgentBase
import gym


class TrainAgent(AgentBase):

    OWN_POS = 0, 0

    def __init__(self, world, creature):
        self.vision_range = 3
        self.grass = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        self.walkable = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        self.other_creatures = np.array([np.array([len([]) for _ in range(self.vision_range * 2 +1)]) for _ in range(self.vision_range * 2 + 1)])
        self.action = 0
        creature.color=(255,255,255)
        super(TrainAgent, self).__init__(world, creature)

    def step(self):
        """Runs through logic to decide next action."""

        valid = self.creature.request_action(self.action)
        assert valid, 'Invalid action!'

    def tick(self):
        survive = True
        if self.creature.get_food()<=0:
            survive=False
        return survive

    def logic(self):
        """Decides what action to take next"""
        self.vision()
        if self.creature.get_food() > 0.8:
            return Creature.REPRODUCE

        if self.creature.get_food() < 1 and self.get_grass(self.OWN_POS) > 0.05:
            return Creature.EAT

        grass_direction = self.best_direction(self, self.OWN_POS)
        return self.move(grass_direction)
    
    def reset(self):
        self.food = 1


    def move(self, direction):
        """Move in given direction if facing the right way, else turn towards that direction"""
        if self.creature.d == direction:
            return Creature.WALK
        if self.creature.d - direction == 1:
            return Creature.TURN_L
        return Creature.TURN_R

    @staticmethod
    def best_direction(self,pos):
        punktN=(pos[0],pos[1]-1)
        punktE=(pos[0]+1,pos[1])
        punktS=(pos[0],pos[1]+1)
        punktW=(pos[0]-1,pos[1])
        n_value=self.get_grass((pos[0],pos[1]-1))
        e_value=self.get_grass((pos[0]+1,pos[1]))
        s_value=self.get_grass((pos[0],pos[1]+1))
        w_value=self.get_grass((pos[0]-1,pos[1]))

        #Sjekker om andre creatures
        if len(self.other_creatures[pos[0]][pos[1]-1])>=1:
            for creature in (self.other_creatures[pos[0]][pos[1]-1]):
                #if creature.get_predator()==True:
                #    n_value-=10
                #else:
                    n_value-=0.7
        if len(self.other_creatures[pos[0]+1][pos[1]])>=1:
            for creature in (self.other_creatures[pos[0]+1][pos[1]]):
                #if creature.get_predator()==True:
                #    e_value-=10
                #else:
                    e_value-=0.7
        if len(self.other_creatures[pos[0]][pos[1]+1])>=1:
            for creature in (self.other_creatures[pos[0]][pos[1]+1]):
                #if creature.get_predator()==True:
                #    s_value-=10
                #else:
                    s_value-=0.7
        if len(self.other_creatures[pos[0]-1][pos[1]])>=1:
            for creature in (self.other_creatures[pos[0]-1][pos[1]]):
                #if creature.get_predator()==True:
                #    w_value-=10
                #else:
                    w_value-=0.7

        #Sjekker om vann
        if self.world.water.is_water(pos[0], pos[1]-1):
            n_value-=0.8
        if self.world.water.is_water(pos[0]+1, pos[1]):
            e_value-=0.8
        if self.world.water.is_water(pos[0], pos[1]+1):
            s_value-=0.8
        if self.world.water.is_water(pos[0]-1, pos[1]):
            w_value-=0.8
        
        values=[n_value,e_value,s_value,w_value]
        bestPoint=max(values)
        if bestPoint==n_value:
            return Creature.N
        if bestPoint==e_value:
            return Creature.E
        if bestPoint==s_value:
            return Creature.S
        if bestPoint==w_value:
            return Creature.W

    def get_grass(self, pos):
        """Get grass value from relative position (i, j)"""
        return self.world.grass.get_value((self.creature.x + pos[0]) % self.world.grid_width,
                                          (self.creature.y + pos[1]) % self.world.grid_height)

    def is_walkable(self, pos):
        """Checks if a tile can be walked on."""
        walkable = True
        if self.world.water.is_water(self.creature.x + pos[0], self.creature.y + pos[1]):
            walkable = False
        occ = [(c.x, c.y) for c in self.world.creatures]
        if (self.creature.x + pos[0], self.creature.y + pos[1]) in occ:
            walkable = False
        return walkable

    def get_creatures(self, pos):
        """Gets creatures in vision range"""
        x_pos = (self.creature.x + pos[0]) % self.world.grid_width
        y_pos = (self.creature.y + pos[1]) % self.world.grid_height
        return len(self.world.creatures_array[x_pos][y_pos])

    def check_grid(self, grid):
        out = None
        if self.creature.y - self.vision_range < 0 and self.creature.x - self.vision_range < 0:
            out = grid[
                  (self.creature.x + self.vision_range + 1) % self.world.grid_width:
                  self.creature.x - self.vision_range,
                  (self.creature.y + self.vision_range + 1) % self.world.grid_height:
                  self.creature.y - self.vision_range]
        elif self.creature.y - self.vision_range < 0:
            out = grid[
                  self.creature.x - self.vision_range:
                  (self.creature.x + self.vision_range + 1) % self.world.grid_width,
                  (self.creature.y + self.vision_range + 1) % self.world.grid_height:
                  self.creature.y - self.vision_range]
        elif self.creature.x - self.vision_range < 0:
            out = grid[
                  (self.creature.x + self.vision_range + 1) % self.world.grid_width:
                  self.creature.x - self.vision_range,
                  self.creature.y - self.vision_range:
                  (self.creature.y + self.vision_range + 1) % self.world.grid_height]
        else:
            out = grid[
                  self.creature.x - self.vision_range:
                  (self.creature.x + self.vision_range + 1) % self.world.grid_width,
                  self.creature.y - self.vision_range:
                  (self.creature.y + self.vision_range + 1) % self.world.grid_height]
        if not out.shape == np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1)).shape:
            out = np.zeros((self.vision_range * 2 + 1, self.vision_range * 2 + 1))
        return out

    def vision(self):
        """Finds grass in vision range, and finds walkable tiles."""
        self.grass = self.check_grid(self.world.grass.grid)
        self.walkable = np.equal(self.check_grid(self.world.water.grid), 0)

        # exit()
        for i in range(-self.vision_range, self.vision_range + 1):
            for j in range(-self.vision_range, self.vision_range + 1):
                #        #self.grass[self.vision_range + i][self.vision_range + j] = self.get_grass((i, j))
                #        self.walkable[self.vision_range + i][self.vision_range + j] = self.is_walkable((i, j))
                self.other_creatures[self.vision_range + i][self.vision_range + j] = self.get_creatures((i, j))

            

    

