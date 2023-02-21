import random

import pygame

from agent import Agent
from t_agent import TAgent
from j_agent import JAgent
from b_agent import BAgent
from rendering import Renderer
from world.world import World, WorldSettings
import time
import wandb


# Grid size is the number of cells in the world
grid_width, grid_height = (40, 20)

# Scale is the pixel size of each world cell on screen
scale = 32

pygame.init()
screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])
    clock = pygame.time.Clock()

    # World setup
    ws = WorldSettings()
    ws.use_temp = True
    ws.grass_growth_rate = 1.1235813*8# Example use of ws

    world = World(grid_width, grid_height, ws)
    renderer = Renderer(world, scale, screen)
    agents = []


    for _ in range(100):
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (50, 50, 50), False)
            agents.append(TAgent(world, c))

   # for _ in range(100):
   #     x = random.randrange(grid_width)
   #     y = random.randrange(grid_height)
   #     if world.water.get_value(x, y) == 0:
   #         c = world.spawn_creature(x, y, (100, 50, 50), False)
   #         agents.append(JAgent(world, c))
    for _ in range(100):
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)
        if world.water.get_value(x, y) == 0:
            c = world.spawn_creature(x, y, (5, 150, 5), False)
            agents.append(BAgent(world, c))

    def reproduction_callback(parent):
        c = world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
        agents.append(parent.agent_type(world, c))

    world.reproduction_callback = reproduction_callback

    running = True
    wandb.init(project="Cogitopia monitor", entity="torghauk-team", config={"growth_rate": ws.grass_growth_rate, "person": "beepboopland", "Temperature": ws.use_temp})
    lastamount = 0
    lasttime = time.time()
    while running:
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step agents
        for agent in agents:
            if agent.world.is_dead(agent.creature):
                #agent.creature.remove_from_array()
                agents.remove(agent)
                #world.creatures.remove(agent.creature)
                pass
            else:
                agent.step()
        # Step world
        world.step()
        j_agentcount = 0
        t_agentcount = 0
        b_agentcount = 0
        for agent in agents:
            if type(agent) == JAgent and not agent.creature.is_dead: j_agentcount += 1
            if type(agent) == TAgent and not agent.creature.is_dead: t_agentcount += 1
            if type(agent) == BAgent and not agent.creature.is_dead: b_agentcount += 1


        wandb.log({"time": world.get_time(),"agentdiff": len(agents)-lastamount, "agentcount": len(agents), "timeuse": time.time()-lasttime, "j_agentcount": j_agentcount, "t_agentcount": t_agentcount, "b_agentcount": b_agentcount})
        lasttime = time.time()
        lastamount = len(agents)
        # Render everything and display
        screen.fill((0, 0, 0))
        renderer.draw_world()
        pygame.display.flip()
        clock.tick(100)
        clock.tick(0)


    pygame.quit()
