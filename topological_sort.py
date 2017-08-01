#!/usr/bin/env python3
from .graph import Node
from .graph import Edge
from .graph import Graph
def topological_sort(graph):
	time = 0

	for node in graph.nodes.values():
		node.is_visited = False
		node.predecessor = None

	def dfs(node):
		nonlocal  time
		time += 1
		node.d = time
		node.is_visited = True
		for node_neighbor in node.neighbors:
			if not node_neighbor.is_visited:
				node_neighbor.predecessor = node
				dfs(node_neighbor)
		time +=1
		node.f = time

	for node in graph.nodes.values():
		if not node.is_visited:
			dfs(node)

	def get_f(node):
		return node.f

	return [node for node in sorted(graph.nodes.values(), key=get_f, reverse=True)]



def topological_sort2(graph):
	time = 0
	nodes = []

	for node in graph.nodes.values():
		node.is_visited = False
		node.predecessor = None

	def dfs(node):
		nonlocal  time
		time += 1
		node.d = time
		node.is_visited = True
		for node_neighbor in node.neighbors:
			if not node_neighbor.is_visited:
				node_neighbor.predecessor = node
				dfs(node_neighbor)
		time +=1
		node.f = time
		nodes.append(node)

	for node in graph.nodes.values():
		if not node.is_visited:
			dfs(node)

	return list(reversed(nodes))

if __name__ == '__main__':
	import cProfile
	from . import generator
	g = generator.DAG(4000,10000000, (1,50))
	cProfile.run('r = topological_sort(g)')
#	print([node.name for node in r])
#	print([[node.name for node in node.neighbors] for node in r])
#	for i, node in enumerate(r):
#		for node_neighbor in node.neighbors:
#			if node_neighbor in r[:i+1]:
#				print('error')
	cProfile.run('r2 = topological_sort2(g)')
#	print([node.name for node in r2])
#	print([[node.name for node in node.neighbors] for node in r2])
#	print(r==r2)
