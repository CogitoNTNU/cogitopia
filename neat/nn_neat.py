from world.world import World
from world.creature import Creature
import os
import neat


#om man ønsker å bruke en tidlgerere generasjon kommenter ut p, og bruk heller load checkpoint
def brain_initialize(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    
    winner = p.run(eval_genomes, 10)

def eval_genomes(genomes, config):
    #TRENGER Å SE ENERGI NIVÅ TIL CREATURE
    pass


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    brain_initialize()