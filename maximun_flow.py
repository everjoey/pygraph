#!/usr/bin/env python3
import numpy

from .graph import Node
from .graph import Edge
from .graph import Graph

def Fold_Fulkerson(flow_network, source, sink, get_path):
	residual_network = Graph()
	residual_network.nodes = {node_name:Node(node_name) for node_name in flow_network.nodes.keys()}
	for edge_name, edge in flow_network.edges.items():
		residual_network.add_edge(Edge(residual_network.nodes[edge_name[0]], residual_network.nodes[edge_name[1]], capacity=edge.capacity))
		residual_network.add_edge(Edge(residual_network.nodes[edge_name[1]], residual_network.nodes[edge_name[0]]))

	augmenting_path = get_path(residual_network, residual_network.nodes[source.name], residual_network.nodes[sink.name])
	while augmenting_path:
		capacity = min(augmenting_path, key=Edge.get_capacity).capacity
		print(len(augmenting_path), capacity)

		for edge in augmenting_path:
			try:
				flow_network.edges[(edge.u.name, edge.v.name)].flow += capacity
			except:
				flow_network.edges[(edge.v.name, edge.u.name)].flow -= capacity
			edge.capacity -= capacity
			residual_network.edges[(edge.v.name, edge.u.name)].capacity += capacity

		augmenting_path = get_path(residual_network, residual_network.nodes[source.name], residual_network.nodes[sink.name])

	print([(edge.capacity, edge.flow) for edge in flow_network.edges.values() if edge.u is source])
	print(sum([edge.flow for edge in flow_network.edges.values() if edge.u is source]))
	print([(edge.capacity, edge.flow) for edge in flow_network.edges.values() if edge.v is sink])
	print(sum([edge.flow for edge in flow_network.edges.values() if edge.v is sink]))

	m = numpy.array([flow_network.edges[(node_name, node_neighbor_name)].flow if flow_network.nodes[node_neighbor_name] in flow_network.nodes[node_name].neighbors else 0 for node_name in flow_network.nodes for node_neighbor_name in flow_network.nodes]).reshape(len(flow_network),len(flow_network))
	print(m)

def get_path(graph, source, sink):
	visited = {node_name:False for node_name in graph.nodes}
	parent = {node_name:None for node_name in graph.nodes}
	q = []
	q.append(source)
	visited[source.name] = True
	path = []
	while q:
		node = q.pop(0)
		for node_neighbor in node.neighbors:
			if graph.edges[(node.name, node_neighbor.name)].capacity == 0:
				continue

			if not visited[node_neighbor.name]:
				q.append(node_neighbor)
				visited[node_neighbor.name] = True
				parent[node_neighbor.name] = node.name

			if node_neighbor is sink:
				'''
				def get_path(sink_name):
					if sink_name is not source.name:
						path.append(graph.edges[(parent[sink_name], sink_name)])
						get_path(parent[sink_name])
				get_path(sink.name)
				'''
				sink_name = sink.name
				while sink_name != source.name:
					path.append(graph.edges[(parent[sink_name], sink_name)])
					sink_name = parent[sink_name]
				return path
	return path

def get_path2(graph, source, sink):
	visited = {node_name:False for node_name in graph.nodes}
	parent = {node_name:None for node_name in graph.nodes}
	def dfs(node):
		if node is sink:
			path = []
			sink_name = sink.name
			while sink_name != source.name:
				path.append(graph.edges[(parent[sink_name], sink_name)])
				sink_name = parent[sink_name]
			return path

		for node_neighbor in node.neighbors:
			if graph.edges[(node.name, node_neighbor.name)].capacity == 0:
				continue

			if not visited[node_neighbor.name]:
				visited[node_neighbor.name] = True
				parent[node_neighbor.name] = node.name
#				print(node.name, node_neighbor.name)
				path = dfs(node_neighbor)
				if path:
					return path
	return dfs(source)
'''
def get_path(graph, source, sink):
	visited = {node_name:False for node_name in graph.nodes}
	parent = {node_name:None for node_name in graph.nodes}
	def dfs(node):
		for node_neighbor in node.neighbors:
			if graph.edges[(node.name, node_neighbor.name)].capacity == 0:
				continue

			if not visited[node_neighbor.name]:
				visited[node_neighbor.name] = True
				parent[node_neighbor.name] = node.name
#				print(node.name, node_neighbor.name)
				dfs(node_neighbor)
	dfs(source)

	path = []
	sink_name = sink.name
	while sink_name != source.name:
		path.append(graph.edges[(parent[sink_name], sink_name)])
		sink_name = parent[sink_name]
	return path
'''

if __name__ == '__main__':
	import cProfile
	from . import generator
	g, s, t = generator.flow_network(200,100000,(1,10))
#	print(g.edges)
#	print([edge_name for edge_name in g.edges])
#	print([g.edges[edge_name].flow for edge_name in g.edges])
#	print([g.edges[edge_name].capacity for edge_name in g.edges])
	cProfile.run('Fold_Fulkerson(g, s, t, get_path2)')
	for edge in g.edges.values():
		edge.flow = 0
	cProfile.run('Fold_Fulkerson(g, s, t, get_path)')

