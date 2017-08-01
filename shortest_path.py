#!/usr/bin/env python3
import math
import functools
import time
import pickle
import cProfile

import numpy as np

from .graph import Node
from .graph import Edge
from .graph import Graph

def clock(func):
	@functools.wraps(func)
	def clocked(*args):
		s = time.time()
		result = func(*args)
		f = time.time()
		print('{0:s} running time: '.format(func.__name__), f-s)
		return result
	return clocked

@clock
def Bellman_Ford(graph, source):
	d = {node_name:float('inf') for node_name in graph.nodes.keys()}
	d[source.name] = 0

	for i in range(len(graph)-1):
		for edge_name, edge in graph.edges.items():
			(node_name, node_neighbor_name) = edge_name
			edge_weight = edge.weight
			value = d[node_name] + edge_weight
			if value < d[node_neighbor_name]:
				d[node_neighbor_name] = value

	for edge_name, edge in graph.edges.items():
		(node_name, node_neighbor_name) = edge_name
		edge_weight = edge.weight
		value = d[node_name] + edge_weight
		if value < d[node_neighbor_name]:
			print('Nagative Cycle')
			return False

	return d



def Bellman_Ford(graph, dst):
	M = [{node_name:0 for node_name in graph.nodes.keys()} for i in range(len(graph))]
	M[0] = {node_name:0 if node_name == dst.name else float('inf') for node_name in graph.nodes.keys()}
	for i in range(1,len(graph)):
		for node_name, node in graph.nodes.items():
			x = [M[i-1][node_neighbor.name] + graph.edges[(node_name, node_neighbor.name)].weight for node_neighbor in node.neighbors]
			M[i][node_name] = min(x+[M[i-1][node_name]])
	return M[-1]



def Bellman_Ford1(graph, dst):
	n = len(graph.nodes)
	W = np.zeros((n, n))
	for i, node_name in enumerate(graph.nodes.keys()):
		for j, neighbor_node_name in enumerate(graph.nodes.keys()):
			if i == j:
				W[i][j] = 0
				continue
			try:
				W[i][j] = graph.edges[(node_name, neighbor_node_name)].weight
			except:
				W[i][j] = float('inf')

	D = np.zeros((n, n, n))

	for i in range(n):
		for j in range(n):
			if i != j:
				D[0][i][j] = float('inf')

	for m in range(1, n):
		for i in range(n):
			for j in range(n):
				d = float('inf')
				for k in range(n):
					d = min(d, W[i][k] + D[m-1][k][j])
				D[m][i][j] = d
	return D[-1]



def Bellman_Ford2(graph, dst):
	n = len(graph.nodes)
	W = np.zeros((n, n))
	for i, node_name in enumerate(graph.nodes.keys()):
		for j, neighbor_node_name in enumerate(graph.nodes.keys()):
			if i == j:
				W[i][j] = 0
				continue
			try:
				W[i][j] = graph.edges[(node_name, neighbor_node_name)].weight
			except:
				W[i][j] = float('inf')

	D_p = W
	m = 1
	while m < len(graph.nodes)-1:
		D = np.zeros((len(graph.nodes), len(graph.nodes)))
		for i, node_name in enumerate(graph.nodes.keys()):
			for j, neighbor_node_name in enumerate(graph.nodes.keys()):
				d = float('inf')
				for k in range(len(graph.nodes)):
					d = min(d, D_p[i][k] + D_p[k][j])
				D[i][j] = d
		m = 2*m
		D_p = D

	return D



class MinHeap(object):
	def __init__(self, x):
		self.x = [None]+x

	def up(self, index):
		if index > 1:
			parent_index = math.floor(index/2)
			if self.x[index].weight < self.x[parent_index].weight:
				self.x[index].index, self.x[parent_index].index = self.x[parent_index].index, self.x[index].index
				self.x[index], self.x[parent_index] = self.x[parent_index], self.x[index]
				self.up(parent_index)

	def down(self, index):
		left_child_index = index*2
		right_child_index = left_child_index+1

		if left_child_index < len(self.x) and right_child_index < len(self.x):
			if self.x[left_child_index].weight < self.x[right_child_index].weight:
				if self.x[index].weight > self.x[left_child_index].weight:
					self.x[index].index, self.x[left_child_index].index = self.x[left_child_index].index, self.x[index].index
					self.x[index], self.x[left_child_index] = self.x[left_child_index], self.x[index]
					self.down(left_child_index)
			else:
				if self.x[index].weight > self.x[right_child_index].weight:
					self.x[index].index, self.x[right_child_index].index = self.x[right_child_index].index, self.x[index].index
					self.x[index], self.x[right_child_index] = self.x[right_child_index], self.x[index]
					self.down(right_child_index)

		elif left_child_index < len(self.x):
			if self.x[index].weight > self.x[left_child_index].weight:
				self.x[index].index, self.x[left_child_index].index = self.x[left_child_index].index, self.x[index].index
				self.x[index], self.x[left_child_index] = self.x[left_child_index], self.x[index]
				self.down(left_child_index)

	def get_min(self):
		self.x[1].index, self.x[-1].index = self.x[-1].index, self.x[1].index
		self.x[1], self.x[-1] = self.x[-1], self.x[1]
		min_value = self.x.pop()
		self.down(1)
		return min_value

	def is_empty(self):
		return len(self.x)==1

@clock
def dijkstra(graph, source):
	d = {}

	for i,node in enumerate(graph.nodes.values(), start=1):
		node.weight = float('inf')
		node.index = i

	q = MinHeap(list(graph.nodes.values()))

	source.weight = 0
	q.up(source.index)

	while not q.is_empty():
		node = q.get_min()

		d[node.name] = node.weight

		for node_neighbor in node.neighbors:
			edge_name = (node.name, node_neighbor.name)
			edge_weight = graph.edges[edge_name].weight
			weight = node.weight + edge_weight
			if weight < node_neighbor.weight:
				node_neighbor.weight = weight
				q.up(node_neighbor.index)
	return d



if __name__ == '__main__':
	import cProfile
	from . import generator
	g = generator.generate(50,500,False,(1,10))
#	print(g.get_adjacency_matrix())
	source = list(g.nodes.values())[0]
	dst = list(g.nodes.values())[-1]
	cProfile.run('d1 = Bellman_Ford1(g, dst)')
	cProfile.run('d2 = Bellman_Ford2(g, dst)')
	cProfile.run('d3 = dijkstra(g, source)')
	print(d1)
	print(d2)
	print(d3)
	print((d1[0] == np.array(list(d3.values()))).all())
