import NeuralNetwork
import GlobalVariables
import HideAndSeek
import numpy
import random
import statistics
import Hider


def reproduce(parent_a: Hider, parent_b: Hider, rate: int):
    return parent_a.reproduce(parent_b.get_genes(), rate)


population_size = 100
mutation_rate = 2
num_generations = 100

# setup - create a population of n elements
population = [GlobalVariables.new_hider() for i in range(population_size)]

gen = 0
final_fitness = 0
scores = []
while gen < num_generations:
    # test population
    HideAndSeek.HideAndSeek(population)

    # calculate fitness of population
    fitness = [x.get_fitness() for x in population]

    # select parents
    median_fitness = numpy.median(fitness)
    reproducers = [hider for hider in population if hider.get_fitness() >= median_fitness]

    # mate reproducers
    population = []
    for parent in reproducers:
        # get the genes from a random reproducer and reproduce
        population.append(reproduce(parent, reproducers[random.randint(0, len(reproducers) - 1)], mutation_rate))
        population.append(reproduce(parent, reproducers[random.randint(0, len(reproducers) - 1)], mutation_rate))

    avg_fit = statistics.mean(fitness)
    print("gen " + str(gen) + "\taverage fitness: " + str(int(avg_fit)) + " ", end='')
    for i in range(int(avg_fit / 2)):
        print("|", end='')
    print("")

    scores.append(avg_fit)
    final_fitness = avg_fit

    # increment generation
    gen += 1

print("generations: " + str(gen))
print("starting fitness: " + str(scores[0])[:5])
print("final fitness: " + str(final_fitness)[:5])
print("percent improvement: " + str(((final_fitness / scores[0]) - 1) * 100)[:5] + "%")
