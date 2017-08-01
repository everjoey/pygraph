#!/usr/bin/env python3
print(__name__)
import random

from .graph import Node
from .graph import Edge
from .graph import Graph
'''
def generate(num_nodes, num_edges, directed=False, weight_range=(1,1)):
	graph = Graph()

	graph.nodes = {i:Node(i) for i in range(num_nodes)}

	edges = [Edge(graph.nodes[i], graph.nodes[j], random.randint(*weight_range)) for i in range(num_nodes) for j in range(num_nodes) if directed or not directed and i<=j]
	random.shuffle(edges)

	for i in range(num_edges):
		graph.add_edge(edges[i])
		if not directed:
			if edges[i].u is not edges[i].v:
				graph.add_edge(Edge(edges[i].v, edges[i].u, edges[i].weight))

#	print(graph.get_adjacency_matrix())
	return graph
'''
def generate(num_nodes, num_edges, directed=False, weight_range=(1,2)):
	graph = Graph()

	graph.nodes = {i:Node(i) for i in range(num_nodes)}

	if len(range(*weight_range)) < num_edges:
		weights = [random.randrange(*weight_range) for i in range(num_edges)]
	else:
		weights = random.sample(range(*weight_range), num_edges)

	edges = [Edge(graph.nodes[i], graph.nodes[j], 0) for i in range(num_nodes) for j in range(num_nodes) if directed or not directed and i<=j]
	edges = random.sample(edges, num_edges)

	for i,edge in enumerate(edges):
		edge.weight = weights[i]
		graph.add_edge(edge)
		if not directed:
			if edge.u is not edge.v:
				graph.add_edge(Edge(edge.v, edge.u, edge.weight))

#	print(graph.get_adjacency_matrix())
	return graph

def complete_graph(num_nodes, directed=False, weight_range=(1,2)):
	num_edges = int((num_nodes-1)*num_nodes) if directed else int((num_nodes-1)*num_nodes/2)

	graph = Graph()
	graph.nodes = {i:Node(i) for i in range(num_nodes)}

	if len(range(*weight_range)) < num_edges:
		weights = [random.randrange(*weight_range) for i in range(num_edges)]
	else:
		weights = random.sample(range(*weight_range), num_edges)

	edges = [Edge(graph.nodes[i], graph.nodes[j]) for i in range(num_nodes) for j in range(num_nodes) if directed or not directed and i<j]

	for i,edge in enumerate(edges):
		edge.weight = weights[i]
		graph.edges[(edge.u.name, edge.v.name)] = edge
		graph.nodes[edge.u.name].neighbors.append(edge.v)
		if not directed:
			graph.edges[(edge.v.name, edge.u.name)] = Edge(edge.v, edge.u, weight=edge.weight)
			graph.nodes[edge.v.name].neighbors.append(edge.u)

#	print(graph.get_adjacency_matrix())
	return graph

def flow_network(num_nodes, num_edges, capacity_range=(0,1)):
	graph = Graph()

	graph.nodes = {i:Node(i) for i in range(num_nodes)}

	if len(range(*capacity_range)) < num_edges:
		capacitys = [random.randrange(*capacity_range) for i in range(num_edges)]
	else:
		capacitys = random.sample(range(*capacity_range), num_edges)

	source_edges_number = random.randrange(1, num_nodes-1)
	source_edges = [Edge(graph.nodes[0], graph.nodes[i]) for i in random.sample(range(1,num_nodes-1), source_edges_number)]

	sink_edges_number = random.randrange(1, num_nodes-1)
	sink_edges = [Edge(graph.nodes[i], graph.nodes[num_nodes-1]) for i in random.sample(range(1,num_nodes-1), sink_edges_number)]

	num_edges = num_edges - source_edges_number - sink_edges_number
	edges = [Edge(*random.sample([graph.nodes[i], graph.nodes[j]],2)) for i in range(1, num_nodes-1) for j in range(1, num_nodes-1) if i<j]
	edges = random.sample(edges, num_edges)+source_edges+sink_edges

	for i,edge in enumerate(edges):
		edge.capacity = capacitys[i]
		edge.flow = 0
		graph.add_edge(edge)

#	print(graph.get_adjacency_matrix())
	return graph, graph.nodes[0], graph.nodes[num_nodes-1]

def DAG(num_nodes, num_edges, weight_range=(0,1)):
	graph = Graph()
	graph.nodes = {node_name:Node(node_name)for node_name in range(num_nodes)}
	nodes = random.sample(range(num_nodes), num_nodes)

	if len(range(*weight_range)) < num_edges:
		weights = [random.randrange(*weight_range) for i in range(num_edges)]
	else:
		weights = random.sample(range(*weight_range), num_edges)

	edges = [(nodes[i], nodes[j]) for i in range(num_nodes) for j in range(i+1, num_nodes)]
	edges = random.sample(edges, num_edges)

	for i,edge_name in enumerate(edges):
		graph.edges[edge_name] = Edge(graph.nodes[edge_name[0]], graph.nodes[edge_name[1]], weights[i])
		graph.nodes[edge_name[0]].neighbors.append(graph.nodes[edge_name[1]])

	return graph

def generate_random_binary_tree(nodes_number, nodes_weight_range=(0,10)):
	graph = Graph()
	graph.nodes = {i:Node(i) for i in range(nodes_number)}
	for node in graph.nodes.values():
		node.weight = random.randrange(*nodes_weight_range)

	nodes = graph.nodes.copy()

	root = graph.nodes[random.randrange(nodes_number)]
	tree = [[root.name]]
	del nodes[root.name]

	i = 0
	while tree[i]:
		tree.append([])
		for tree_node_name in tree[i]:
			tree_node = graph.nodes[tree_node_name]

			left_node_name = random.sample(list(nodes.keys())+[None], 1)[0]
			if left_node_name is not None:
				tree[i+1].append(left_node_name)
				graph.add_edge(Edge(graph.nodes[tree_node_name], graph.nodes[left_node_name]))
				del nodes[left_node_name]
			else:
				tree_node.neighbors.append(None)

			right_node_name = random.sample(list(nodes.keys())+[None], 1)[0]
			if right_node_name is not None:
				tree[i+1].append(right_node_name)
				graph.add_edge(Edge(graph.nodes[tree_node_name], graph.nodes[right_node_name]))
				del nodes[right_node_name]
			else:
				tree_node.neighbors.append(None)

		i+=1

	for tree_layer in tree:
		print([graph.nodes[node_name].weight for node_name in tree_layer])
		for x in tree_layer:
			print([node_neighbor.weight if node_neighbor is not None else node_neighbor for node_neighbor in graph.nodes[x].neighbors])
		print()

	return root

if __name__ == '__main__':
	import time
	import cProfile
#	cProfile.run('g=complete_graph(1000,False,(0,50))')
#	print([edge.weight for edge in g.edges.values()])
	cProfile.run('g1=DAG(1000,10000,(0,50))')
#	print(g.nodes)
