# Evolve a control/reward estimation network for the OpenAI Gym
# LunarLander-v2 environment (https://gym.openai.com/envs/LunarLander-v2).
# Sample run here: https://gym.openai.com/evaluations/eval_FbKq5MxAS9GlvB7W6ioJkg


import multiprocessing
import os
import pickle
import random
import time
import yaml
import git
from NEAT_world import TrainWorld
import gym.wrappers
import matplotlib.pyplot as plt
import wandb
import numpy as np
from world.world import WorldSettings

import neat
#import visualize
ws = WorldSettings()
NUM_CORES = 8
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
env = TrainWorld()


#print("action space: {0!r}".format(env.action_space))
#print("observation space: {0!r}".format(env.observation_space))


class LanderGenome(neat.DefaultGenome):
    def __init__(self, key):
        super().__init__(key)
        self.discount = None

    def configure_new(self, config):
        super().configure_new(config)
        self.discount = 0.01 + 0.98 * random.random()

    def configure_crossover(self, genome1, genome2, config):
        super().configure_crossover(genome1, genome2, config)
        self.discount = random.choice((genome1.discount, genome2.discount))

    def mutate(self, config):
        super().mutate(config)
        self.discount += random.gauss(0.0, 0.05)
        self.discount = max(0.01, min(0.99, self.discount))

    def distance(self, other, config):
        dist = super().distance(other, config)
        disc_diff = abs(self.discount - other.discount)
        return dist + disc_diff

    def __str__(self):
        return f"Reward discount: {self.discount}\n{super().__str__()}"


def compute_fitness(genome, net, episodes, min_reward, max_reward):
    env = TrainWorld()
    data = []
    for i in range(1):
        observation = [env.reset()]
        step = 0
        while 1:
            step += 1

            actions = []
            output = net.activate(observation[0].flatten())
            actions.append(np.argmax(output))

            for i in range(min(len(observation) - 1, len(env.agents))):
                output = net.activate(observation[i + 1].flatten())
                actions.append(np.argmax(output))

            if actions[0] != 0: print(actions[0])
            observation, reward, done, info = env.step(actions)
            data.append(np.hstack((observation[0].flatten(), actions[0], reward)))

            if done:
                break

    data = np.array(data)
    score = np.sum(data[:, -1])/2
    return score


class PooledErrorCompute(object):
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.test_episodes = []
        self.generation = 0

        self.min_reward = -200
        self.max_reward = 200

        self.episode_score = []
        self.episode_length = []

    def simulate(self, nets):
        scores = []
        with multiprocessing.Pool(self.num_workers) as pool:
            jobs = []
            for genome, net in nets:
                jobs.append(pool.apply_async(compute_fitness,
                                             (genome, net, self.test_episodes,
                                              self.min_reward, self.max_reward)))

            for job, (genome_id, genome) in zip(jobs, nets):
                reward = job.get(timeout=None)
                scores.append(reward)
        self.episode_score = scores


        print("Score range [{:.3f}, {:.3f}]".format(min(scores), max(scores)))

    def evaluate_genomes(self, genomes, config):
        self.generation += 1

        t0 = time.time()
        nets = []
        for gid, g in genomes:
            nets.append((g, neat.nn.FeedForwardNetwork.create(g, config)))

        print("network creation time {0}".format(time.time() - t0))
        t0 = time.time()
        self.simulate(nets)

        # Periodically generate a new set of episodes for comparison.
        if 1 == self.generation % 10:
            self.test_episodes = self.test_episodes[-300:]
            self.simulate(nets)
            print("simulation run time {0}".format(time.time() - t0))
            t0 = time.time()

        # Assign a composite fitness to each genome; genomes can make progress either
        # by improving their total reward or by making more accurate reward estimates.
        print("Evaluating {0} test episodes".format(len(self.test_episodes)))
     #   if self.num_workers < 2:
        genome_num = 0
        best_fitness = -1e100
        for genome, net in nets:
            #reward_error = compute_fitness(genome, net, self.test_episodes, self.min_reward, self.max_reward)
            genome.fitness = np.sum(self.episode_score[genome_num])
            genome_num+=1
            if genome.fitness > best_fitness: best_fitness = genome.fitness
        wandb.log(best_fitness)

   #    else:
   #        with multiprocessing.Pool(self.num_workers) as pool:
   #            jobs = []
   #            for genome, net in nets:
   #                jobs.append(pool.apply_async(compute_fitness,
   #                                             (genome, net, self.test_episodes,
   #                                              self.min_reward, self.max_reward)))

   #            for job, (genome_id, genome) in zip(jobs, genomes):
   #                reward_error = job.get(timeout=None)
   #                genome.fitness = -np.sum(reward_error) / len(self.test_episodes)

   #    print("final fitness compute time {0}\n".format(time.time() - t0))


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'NEATconfig')
    config = neat.Config(LanderGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    # Checkpoint every 25 generations or 900 seconds.
    pop.add_reporter(neat.Checkpointer(25, 900))

    # Run until the winner from a generation is able to solve the environment
    # or the user interrupts the process.
    ec = PooledErrorCompute(NUM_CORES)
    while 1:
        wandb.init(project="Cogitopia NEAT monitor",
                   entity="torghauk-team",
                   config={"growth_rate": ws.grass_growth_rate,
                           "git_hash": sha,
                           "world_settings": ws.settings})
        try:
            gen_best = pop.run(ec.evaluate_genomes, 7)
            wandb.log(len(pop.species))

            # print(gen_best)

            #visualize.plot_stats(stats, ylog=False, view=False, filename="fitness.svg")

#            plt.plot(ec.episode_score, 'g-', label='score')
#            plt.plot(ec.episode_length, 'b-', label='length')
#            plt.grid()
#            plt.legend(loc='best')
#            plt.savefig("scores.svg")
#            plt.close()

            mfs = sum(stats.get_fitness_mean()[-5:]) / 5.0
            print("Average mean fitness over last 5 generations: {0}".format(mfs))

            mfs = sum(stats.get_fitness_stat(min)[-5:]) / 5.0
            print("Average min fitness over last 5 generations: {0}".format(mfs))

            # Use the best genomes seen so far as an ensemble-ish control system.
            best_genomes = stats.best_unique_genomes(3)
            best_networks = []
            for g in best_genomes:
                best_networks.append(neat.nn.FeedForwardNetwork.create(g, config))

            solved = True
            best_scores = []
            for k in range(100):
                observation = [env.reset()]
                score = 0
                step = 0
                while 1:
                    step += 1
                    # Use the total reward estimates from all five networks to
                    # determine the best action given the current state.
                    actions = []
                    votes = np.zeros((8,))
                    for n in best_networks:
                        output = n.activate(observation[0].flatten())
                        votes[np.argmax(output)] += 1

                    actions.append(np.argmax(votes))
                    for i in range(min(len(observation)-1, len(env.agents))):
                        votes = np.zeros((8,))
                        for n in best_networks:
                            output = n.activate(observation[i+1].flatten())
                            votes[np.argmax(output)] += 1

                        actions.append(np.argmax(votes))


                    observation, reward, done, info = env.step(actions)
                    score += reward
                    #env.render()
                    if done:
                        break

                ec.episode_score.append(score)
                ec.episode_length.append(step)

                best_scores.append(score)
                avg_score = sum(best_scores) / len(best_scores)
                print(k, score, avg_score)
                if avg_score < 200:
                    solved = False
                    break

            if solved:
                print("Solved.")

                # Save the winners.
                for n, g in enumerate(best_genomes):
                    name = 'winner-{0}'.format(n)
                    with open(name + '.pickle', 'wb') as f:
                        pickle.dump(g, f)

                    #visualize.draw_net(config, g, view=False, filename=name + "-net.gv")
                    #visualize.draw_net(config, g, view=False, filename=name + "-net-pruned.gv", prune_unused=True)

                break
        except KeyboardInterrupt:
            print("User break.")
            break

    env.close()


if __name__ == '__main__':
    run()