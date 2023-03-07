
class AgentBase:
    def __init__(self, world, creature):
        self.world = world
        self.creature = creature
        self.creature.agent_type = type(self)

    def check_creature(self):
        if self.creature is None or self.creature.is_dead:
            return False
        return True
