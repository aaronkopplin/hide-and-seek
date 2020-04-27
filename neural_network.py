import random
import numpy
import math

class neural_network():
	def __init__(self, num_input_nodes, nodes_in_hidden_layer, num_output_nodes):
		self.input_nodes = []
		self.hidden_layer_nodes = []
		self.output_nodes = []
		self.time_alive = 0 # for calculating fitness

		for i in range(num_input_nodes):
			# left is none because this is the left side of the graph
			self.input_nodes.append(neuron(None, []))

		for i in range(num_output_nodes):
			# right is none because this is the right side of the graph
			self.output_nodes.append(neuron([], None))

		for i in range(nodes_in_hidden_layer):
			self.hidden_layer_nodes.append(neuron([], []))
			mid_node = self.hidden_layer_nodes[i]

			for in_node in self.input_nodes:
				syn = synapse(in_node, mid_node)

			for out_node in self.output_nodes:
				syn = synapse(mid_node, out_node)

	def get_fitness(self):
		return self.time_alive

	def __str__(self):
		ret = ""
		for n in self.input_nodes:
			ret += n.__str__()

		for n in self.hidden_layer_nodes:
			ret += n.__str__()

		for n in self.output_nodes:
			ret += n.__str__()

		return ret

	def fire(self):
		for n in self.hidden_layer_nodes:
			n.activate()

		for n in self.output_nodes:
			n.activate()

	def input(self, values):
		self.time_alive += 1
		
		for i in range(len(self.input_nodes)):
			self.input_nodes[i].value = values[i]

		self.fire()

	def get_output(self):
		ret = []
		for n in self.output_nodes:
			ret.append(n.value)

		return ret

	def get_genes(self):
		temp = self.input_nodes
		temp += self.hidden_layer_nodes
		for n in self.hidden_layer_nodes:
			temp += n.right_synapses
			temp += n.left_synapses

		temp += self.output_nodes

		return temp

	def mutate(self):
		random.choice(self.get_genes()).reset_gene


class synapse():
	def __init__(self, left_node, right_node):
		self.weight = random.uniform(-1, 1)
		self.left_node = left_node
		self.left_node.add_synapse("right", self)
		self.right_node = right_node
		self.right_node.add_synapse("left", self)

	def reset_gene(self):
		self.weight = random.uniform(-1,1)

	def __str__(self):
		return "weight: " + str(self.weight)[:7] + " " 

class neuron():
	def __init__(self, left_synapses, right_synapses):
		self.bias = random.uniform(-1, 1)
		self.value = 0
		self.left_synapses = left_synapses # list of connections
		self.right_synapses = right_synapses # list of connections

	def sigmoid(self, x):
		return 1 / (1 + math.exp(-x))

	def add_synapse(self, string, synapse):
		if(string == "left"):
			self.left_synapses.append(synapse)
		elif (string == "right"):
			self.right_synapses.append(synapse)
		else:
			print("ERROR")

	def activate(self):
		tot = 0
		for s in self.left_synapses:
			tot += s.weight * s.left_node.value

		self.value = self.sigmoid(tot + self.bias)

	def reset_gene(self):
		self.bias = random.uniform(-1, 1)

	def __str__(self):
		ls = ""
		if self.left_synapses != None:
			for s in self.left_synapses:
				ls += s.__str__() + " "

		rs = ""
		if self.right_synapses != None:
			for s in self.right_synapses:
				rs += s.__str__() + " "

		return "bias: " + str(self.bias)[:7] + "\t" + "left: " + ls + "\t" + "right: " + rs + "value: " + str(self.value) + "\n"
