
class AgentBase:
    def __init__(self, world, creature):
        self.world = world
        self.creature = creature
        self.creature.agent_type = type(self)
