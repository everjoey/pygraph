#!/usr/bin/env python3
print(__name__)
import copy
import functools
import numpy

def clock(func):
	@functools.wraps(func)
	def clocked(*args):
		s = time.time()
		result = func(*args)
		f = time.time()
		print('{0:s} running time: '.format(func.__name__), f-s)
		return result
	return clocked

'''
class clock(object):
	def __init__(self, f):
		self.f = f

	def __call__(self, *args):
		print(args)
		start = time.time()
		result = self.f(*args)
		finish = time.time()
		print(finish - start)
		return result
'''

class Node(object):
	def __init__(self, name, neighbors=[]):
		self.name = name
		self.neighbors = neighbors.copy()

#	def __eq__(self, other):
#		return id(self) == id(other)

#	def __repr__(self):
#		return str(self.name)



class Edge(object):
	def __init__(self, u, v, weight=0, capacity=0):
		self.u = u
		self.v = v
		self.weight = weight
		self.capacity = capacity

#	def __repr__(self):
#		return str((self.u.name ,self.v.name))

	def get_weight(self):
		return self.weight

	def get_capacity(self):
		return self.capacity

class Graph(object):
	def __init__(self):
		self.nodes = {}
		self.edges = {}

	def __len__(self):
		return len(self.nodes)

	def get_adjacency_matrix(self):
		return numpy.array([1 if self.nodes[node_neighbor_name] in self.nodes[node_name].neighbors else 0 for node_name in self.nodes for node_neighbor_name in self.nodes]).reshape(len(self),len(self))

	def add_node(self, node):
		if node.name not in self.nodes:
#			self.nodes.append(node)
			self.nodes[node.name] = node
		else:
			raise KeyError('the node already exists')

	def add_edge(self, edge):
		if edge.u.name in self.nodes and edge.v.name in self.nodes:
			if edge.v in edge.u.neighbors:
				raise KeyError('the edge already exists')
			else:
				edge.u.neighbors.append(edge.v)
#				self.edges.append(edge)
				self.edges[(edge.u.name, edge.v.name)] = edge
		else:
			raise KeyError('the nodes of the edge does not exist on the graph.')
	'''
	def delete_node(self, node):
		self.nodes.remove(node)
		for other_node in self.nodes:
#			try:
#				other_node.neighbors.remove(node)
#			except:
#				pass
			if node in other_node.neighbors:
				other_node.neighbors.remove(node)

		self.edges = [edge for edge in self.edges if edge.u is not node and edge.v is not node]
	'''
	'''
	def delete_edge(self, edge):
		self.edges.remove(edge)
		u = edge.u
		v = edge.v
		u.neighbors.remove(v)
	'''
	'''
	def copy(self):
		return copy.deepcopy(self)
	'''
if __name__ == '__main__':
	n1 = Node('A')
	n2 = Node('B')
	n3 = Node('C')
	n4 = Node('C')
	g = Graph()
	g.add_node(n1)
	print(g.nodes)
	g.add_node(n1)
	print(g.nodes)
