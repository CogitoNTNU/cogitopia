import random
import time
import git
import pygame
import wandb

from t_agent import TAgent
from j_agent import JAgent
from b_agent import BAgent
from rendering import Renderer
from world.world import World, WorldSettings

if __name__ == '__main__':
    ws = WorldSettings()

    # Grid size is the number of cells in the world
    grid_width, grid_height = (ws.grid_width, ws.grid_height)

    # Scale is the pixel size of each world cell on screen
    scale = ws.scale

    pygame.init()
    screen = pygame.display.set_mode([grid_width * scale, grid_height * scale])
    clock = pygame.time.Clock()

    # World setup
    world = World(grid_width, grid_height, ws)
    renderer = Renderer(world, scale, screen)
    agents = []

    # Get git commit hash
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    # wandb.init(project="Cogitopia monitor",
    #            entity="torghauk-team",
    #            config={"growth_rate": ws.grass_growth_rate,
    #                    "git_hash": sha,
    #                    "world_settings": ws.settings})

    def spawn(amount, agent_type):
        for _ in range(amount):
            x_pos = random.randrange(grid_width)
            y_pos = random.randrange(grid_height)
            if world.water.get_value(x_pos, y_pos) == 0:
                creature = world.spawn_creature(x_pos, y_pos, agent_type.COLOR, agent_type.IS_PREDATOR)
                agents.append(agent_type(world, creature))

    #spawn(ws.j_agent_amount, JAgent)
    #spawn(ws.t_agent_amount, TAgent)
    #spawn(ws.b_agent_amount, BAgent)

    def reproduction_callback(parent):
        c = world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
        agents.append(parent.agent_type(world, c))


    world.reproduction_callback = reproduction_callback


    running = True


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
                # agent.creature.remove_from_array()
                agents.remove(agent)
                # world.creatures.remove(agent.creature)
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

        # wandb.log({"time": world.get_time(), "agentdiff": len(agents) - lastamount, "agentcount": len(agents),
        #            "timeuse": time.time() - lasttime, "j_agentcount": j_agentcount, "t_agentcount": t_agentcount,
        #            "b_agentcount": b_agentcount})
        lasttime = time.time()
        lastamount = len(agents)
        # Render everything and display
        screen.fill((0, 0, 0))
        renderer.draw_world()
        pygame.display.flip()
        clock.tick(ws.clock_speed)

    pygame.quit()
