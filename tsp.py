#!/usr/bin/env python3
from .graph import Node
from .graph import Edge
from .graph import Graph

import itertools

def brute_force(graph):
	min_path_weight = float('inf')
	for path in itertools.permutations(graph.nodes.keys(), len(graph.nodes)):
		path_weight = 0
		for i, u_name in enumerate(path):
			v_name = path[0] if i == len(path)-1 else path[i+1]
			path_weight += graph.edges[(u_name, v_name)].weight
		print(path_weight)
		print(path)
		if path_weight < min_path_weight:
			min_path_weight = path_weight
			min_path = path
	return min_path_weight, min_path

if __name__ == '__main__':
	from . import generator
	import cProfile
	g = generator.complete_graph(15, False, (0,10))
	pw = brute_force(g)
	print('min', pw)
