import random
import gym
import time
import git
import pygame
import wandb
from wandb.integration.sb3 import WandbCallback

from agents.t_agent import TAgent
from agents.j_agent import JAgent
from agents.b_agent import BAgent
from agents.sau_agent import SauAgent
from ppo_agent import PPOAgent, PPOAgentPred
from rendering import Renderer
from world.world import World, WorldSettings
from stable_baselines3.common.vec_env import VecMonitor

if __name__ == '__main__':
    ws = WorldSettings()

from stable_baselines3 import PPO
from stable_baselines3.common.logger import configure
from stable_baselines3.common.env_util import make_vec_env
from agents.train import TrainAgent
from train_world import TrainWorld

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

trainrun = wandb.init(project="Cogitopia ppovision",
           entity="torghauk-team",
                      sync_tensorboard=True,
           config={"growth_rate": ws.grass_growth_rate,
                   "git_hash": sha,
                   "world_settings": ws.settings})

def spawn(amount, agent_type):
    for _ in range(amount):
        x_pos = random.randrange(grid_width)
        y_pos = random.randrange(grid_height)
        if world.water.get_value(x_pos, y_pos) == 0:
            creature = world.spawn_creature(x_pos, y_pos, agent_type.COLOR, agent_type.IS_PREDATOR)
            agents.append(agent_type(world, creature))
env = make_vec_env(TrainWorld, n_envs=2)
env = VecMonitor(env)
#env = agent


new_logger = configure('./results', ["stdout", "csv", "json", "log"])
#model = PPO("MlpPolicy", env, 1/50000, verbose=1)
#model.set_parameters("ppo_agent2.zip")
#model.set_logger(new_logger)
#model.learn(total_timesteps=500, log_interval=4,
#            callback=WandbCallback(
#                gradient_save_freq=1000,
#                verbose=2,
#                log="all"
#            ))
#model.save("ppo_agent2")

trainrun.finish()
total_len = 0
num_episodes = 0
spawn(ws.j_agent_amount, JAgent)
spawn(ws.t_agent_amount, TAgent)
spawn(ws.b_agent_amount, BAgent)
spawn(20, PPOAgent)
spawn(20, PPOAgentPred)
obs = env.reset()

def reproduction_callback(parent):
    c = world.spawn_creature(parent.x, parent.y, parent.color, parent.predator)
    agents.append(parent.agent_type(world, c))


world.reproduction_callback = reproduction_callback


running = True
wandb.init(project="Cogitopia monitor",
           entity="torghauk-team",
           config={"growth_rate": ws.grass_growth_rate,
                   "git_hash": sha,
                   "world_settings": ws.settings})

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
    sau_agentcount = 0
    ppo_agentcount = 0
    ppo_agent_predcount = 0
    for agent in agents:
        if type(agent) == JAgent and not agent.creature.is_dead: j_agentcount += 1
        if type(agent) == TAgent and not agent.creature.is_dead: t_agentcount += 1
        if type(agent) == BAgent and not agent.creature.is_dead: b_agentcount += 1
        if type(agent) == SauAgent and not agent.creature.is_dead: sau_agentcount += 1
        if type(agent) == PPOAgent and not agent.creature.is_dead: ppo_agentcount += 1
        if type(agent) == PPOAgentPred and not agent.creature.is_dead: ppo_agent_predcount += 1

    wandb.log({"time": world.get_time(), "agentdiff": len(agents) - lastamount, "agentcount": len(agents),
               "timeuse": time.time() - lasttime, "j_agentcount": j_agentcount, "t_agentcount": t_agentcount,
               "b_agentcount": b_agentcount, "ppo_agentcount": ppo_agentcount,"ppo_agent_predcount": ppo_agent_predcount})
    lasttime = time.time()
    lastamount = len(agents)
    # Render everything and display
    screen.fill((0, 0, 0))
    renderer.draw_world()
    pygame.display.flip()
    clock.tick(ws.clock_speed)

pygame.quit()
