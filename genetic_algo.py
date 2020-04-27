import neural_network as nn
import global_vars as gv
import hide_and_seek as hs
import numpy
import random
import statistics

######################################################################
# methods
######################################################################

def create_population(pop_size):
	population = []
	for i in range(pop_size):
		population.append(nn.neural_network(4, 8, 4))

	return population

def splice(list_a, list_b):
	spliced_list = []
	a = True
	for i in range(len(list_a)):
		if a:
			spliced_list.append(list_a[i])
		else:
			spliced_list.append(list_b[i])
		a = not a

	return spliced_list

def reproduce(a, b):
	child = nn.neural_network(4, 8, 4)
	child.input_nodes = splice(a.input_nodes, b.input_nodes)
	child.hidden_layer_nodes = splice(a.hidden_layer_nodes, b.hidden_layer_nodes)
	child.output_nodes = splice(a.output_nodes, b.output_nodes)

	child.mutate()

	return child

def calculate_fitness(pop):
	fitness = []
	round = 0
	for n in pop:
		hs.window(n)
		# print("round: " + str(round) + "\tscore: " + str(n.time_alive))
		round += 1
		fitness.append(n.get_fitness())

	return fitness

def select_reproducers(fitness, pop):
	reproducers = []
	median = numpy.median(fitness)
	for n in pop:
		if n.time_alive > median:
			reproducers.append(n)

	return reproducers

def new_generation(reproducers):
	next_population = []
	for r in reproducers:
		# have two children
		next_population.append(reproduce(r, random.choice(reproducers)))
		next_population.append(reproduce(r, random.choice(reproducers)))

	return next_population



######################################################################
# algorithm
######################################################################

population_size = 50
mutation_rate = .01
num_generations = 100

# setup - create a population of n elements
population = create_population(population_size)

gen = 0
while gen < num_generations:
	# calculate fitness
	fitness = calculate_fitness(population)

	# select parents
	reproducers = select_reproducers(fitness, population)

	# mate parents
	population = new_generation(reproducers)

	print("gen " + str(gen) + "\taverage fitness: " + str(statistics.mean(fitness)))

