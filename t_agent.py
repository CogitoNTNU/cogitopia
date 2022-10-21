from world.creature import Creature


class TAgent:
    def __init__(self, world, creature):
        self.world = world
        self.creature = creature

    def step(self):
        valid = False
        turn = 0
        while not valid:
            action = self.logic()
            valid = self.creature.request_action(action)
            turn += 1
            print(turn)
            print(action)

    def logic(self):
        # Find best grass
        # Find path
        # Find direction to go
        x = self.creature.x
        y = self.creature.y
        max_grass = self.world.grass.get_value(x, y)
        grass_pos = x, y
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j == 0:
                    continue
                value = self.world.grass.get_value((x + i) % self.world.size, (y + j) % self.world.size)
                if value > max_grass and not self.world.water.is_water(x + i, y + j):
                    max_grass = value
                    grass_pos = (x + i) % self.world.size, (y + j) % self.world.size

        if self.creature.get_food() < 0.3 and self.world.grass.get_value(x, y) > 0.05:
            return Creature.EAT
        if value > 0.05:
            if grass_pos[0] < x:
                if self.creature.d == self.creature.W:
                    return Creature.WALK
                if self.creature.d == self.creature.N:
                    return Creature.TURN_L
                return Creature.TURN_R

            if grass_pos[0] > x:
                if self.creature.d == self.creature.E:
                    return Creature.WALK
                if self.creature.d == self.creature.N:
                    return Creature.TURN_R
                return Creature.TURN_L

            if grass_pos[0] > y:
                if self.creature.d == self.creature.N:
                    return Creature.WALK
                if self.creature.d == self.creature.W:
                    return Creature.TURN_R
                return Creature.TURN_L

            if grass_pos[0] < y:
                if self.creature.d == self.creature.S:
                    return Creature.WALK
                if self.creature.d == self.creature.E:
                    return Creature.TURN_R
                return Creature.TURN_L
        return Creature.STAY
