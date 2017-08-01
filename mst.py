#!/usr/bin/env python3
################################################################
####	This is a python file which include two
####	algoritms of minimun spanning tree.
################################################################
import math
import functools
import time

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

class MinHeap2(list):
	def __setitem__(self, key, value):
		super().__setitem__(key, value)
		value.index = key

	def up(self, index):
		if index > 1:
			parent_index = math.floor(index/2)
			if self[index].weight < self[parent_index].weight:
				self[index], self[parent_index] = self[parent_index], self[index]
				self.up(parent_index)

	def down(self, index):
#		right_child_index = (index+1)*2
#		left_child_index = right_child_index-1
		left_child_index = index*2
		right_child_index = left_child_index+1

		if left_child_index < len(self) and right_child_index < len(self):
			if self[left_child_index].weight < self[right_child_index].weight:
				if self[index].weight > self[left_child_index].weight:
					self[index], self[left_child_index] = self[left_child_index], self[index]
					self.down(left_child_index)
			else:
				if self[index].weight > self[right_child_index].weight:
					self[index], self[right_child_index] = self[right_child_index], self[index]
					self.down(right_child_index)

		elif left_child_index < len(self):
			if self[index].weight > self[left_child_index].weight:
				self[index], self[left_child_index] = self[left_child_index], self[index]
				self.down(left_child_index)

	def extract_min(self):
		self[1], self[-1] = self[-1], self[1]
		min_value = self.pop()
		self.down(1)
		return min_value

	def is_empty(self):
		return len(self)==1

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
def Prim(graph, source):
	'''
	running time: O((V+E)logV)
	'''
	tree = Graph()
	tree.nodes = {node_name:Node(node_name) for node_name in graph.nodes}

	for i,node in enumerate(graph.nodes.values(), start=1):
		node.weight = float('inf')
		node.parent = None
		node.index = i

	q = MinHeap2([None]+list(graph.nodes.values()))

	while not q.is_empty():
		node = q.extract_min()

		if node.parent is not None:
			tree.add_edge(Edge(tree.nodes[node.name], tree.nodes[node.parent.name], node.weight))
			tree.add_edge(Edge(tree.nodes[node.parent.name], tree.nodes[node.name], node.weight))

		for node_neighbor in node.neighbors:
			if node_neighbor.index != -1:
				edge_name = (node.name, node_neighbor.name)
				edge_weight = graph.edges[edge_name].weight
				if edge_weight < node_neighbor.weight:
					node_neighbor.weight = edge_weight
					node_neighbor.parent = node
					q.up(node_neighbor.index)

#	for node in graph.nodes.values():
#		if node.parent is not None:
#			tree.add_edge(Edge(tree.nodes[node.name], tree.nodes[node.parent.name], node.weight))
#			tree.add_edge(Edge(tree.nodes[node.parent.name], tree.nodes[node.name], node.weight))

	print(sum([edge.weight for edge in tree.edges.values()]))
	return tree.edges

@clock
def Prim_old(graph, source):
	'''
	running time: O((V+E)logV)
	'''
	tree = Graph()
	tree.nodes = {node_name:Node(node_name) for node_name in graph.nodes}

	for i,node in enumerate(graph.nodes.values(), start=1):
		node.weight = float('inf')
		node.parent = None
		node.index = i

	q = MinHeap(list(graph.nodes.values()))

	while not q.is_empty():
		node = q.get_min()

		if node.parent is not None:
			tree.add_edge(Edge(tree.nodes[node.name], tree.nodes[node.parent.name], node.weight))
			tree.add_edge(Edge(tree.nodes[node.parent.name], tree.nodes[node.name], node.weight))

		for node_neighbor in node.neighbors:
			if node_neighbor.index < len(q.x):
				edge_name = (node.name, node_neighbor.name)
				edge_weight = graph.edges[edge_name].weight
				if edge_weight < node_neighbor.weight:
					node_neighbor.weight = edge_weight
					node_neighbor.parent = node
					q.up(node_neighbor.index)

#	for node in graph.nodes.values():
#		if node.parent is not None:
#			tree.add_edge(Edge(tree.nodes[node.name], tree.nodes[node.parent.name], node.weight))
#			tree.add_edge(Edge(tree.nodes[node.parent.name], tree.nodes[node.name], node.weight))

	print(sum([edge.weight for edge in tree.edges.values()]))
	return tree.edges

@clock
def Prim2(graph, source):
	tree = Graph()
	tree.nodes = {node_name:Node(node_name) for node_name in graph.nodes}

	for node in graph.nodes.values():
		node.weight = float('inf')
		node.parent = None

	q = graph.nodes.copy()

	def get_weight(node):
		return node.weight

	while q:
		node = min(q.values(), key=get_weight)
		del q[node.name]

		if node.parent is not None:
			tree.add_edge(Edge(tree.nodes[node.name], tree.nodes[node.parent.name], node.weight))
			tree.add_edge(Edge(tree.nodes[node.parent.name], tree.nodes[node.name], node.weight))

		for node_neighbor in node.neighbors:
			if node_neighbor.name in q:
				edge_name = (node.name, node_neighbor.name)
				edge_weight = graph.edges[edge_name].weight
				if edge_weight < node_neighbor.weight:
					node_neighbor.weight = edge_weight
					node_neighbor.parent = node

	print(sum([edge.weight for edge in tree.edges.values()]))
	return tree.edges

@clock
def kruskal(graph):
	tree = Graph()
	tree.nodes = {node_name:Node(node_name) for node_name in graph.nodes}

	#create and initialize some attributes of the node
	for node in graph.nodes.values():
		node.parent = node
		node.rank = 0

	def find_set(node):
		if node != node.parent:
			node.parent = find_set(node.parent)
		return node.parent

	def union(x,y):
		link(find_set(x), find_set(y))

	def link(x,y):
		if x.rank > y.rank:
			y.parent = x
		else:
			x.parent = y
			if x.rank == y.rank:
				y.rank+=1

	for edge in sorted(graph.edges.values(), key=Edge.get_weight):
		u = edge.u
		v = edge.v
		if find_set(u) != find_set(v):
			tree.add_edge(Edge(tree.nodes[u.name], tree.nodes[v.name], edge.weight))
			tree.add_edge(Edge(tree.nodes[v.name], tree.nodes[u.name], edge.weight))
			union(u, v)

	print(sum([edge.weight for edge in tree.edges.values()]))
	return tree.edges



if __name__ == '__main__':
	import cProfile
	from . import generator
	g = generator.generate(2000,30000,False,(1,100000))
#	print(g.get_adjacency_matrix())
	cProfile.run('r1 = Prim(g,1)')
	cProfile.run('r2 = Prim2(g,0)')
	cProfile.run('r3 = kruskal(g)')
	cProfile.run('r4 = Prim_old(g,1)')
	print(r1.keys() == r2.keys())
	print(r2.keys() == r3.keys())

        print()

	'''
	h1 = MinHeap([])
	h2 = MinHeap2([None])
	def f():
		print(h1)
		for i in range(1000000):
			h1.x.append(Node(i))
		for i in range(1,1000000-1):
			h1.x[i], h1.x[i+1] = h1.x[i+1], h1.x[i]
	cProfile.run('f()')

	def g():
		print(h2)
		for i in range(1000000):
			h2.append(Node(i))
		for i in range(1,1000000-1):
			h2[i], h2[i+1] = h2[i+1], h2[i]
	cProfile.run('g()')
	'''
