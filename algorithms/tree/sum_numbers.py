#!/usr/bin/env python3

def binary_tree_has_path_sum(root, path_sum):
	if root is None:
		return False
	elif not any(root.neighbors):
		return root.weight == path_sum
	else:
		left = binary_tree_has_path_sum(root.neighbors[0], path_sum - root.weight)
		right = binary_tree_has_path_sum(root.neighbors[1], path_sum - root.weight)
		return left or right

def binary_tree_path_sum(root, path_sum):
	if root is None:
		return []
	elif not any(root.neighbors):
		if root.weight == path_sum:
			return [[root.weight]]
		else:
			return []
	else:
		left_paths = binary_tree_path_sum(root.neighbors[0], path_sum - root.weight)
		right_paths = binary_tree_path_sum(root.neighbors[1], path_sum - root.weight)
		return [[root.weight] + path for path in left_paths] + [[root.weight] + path for path in right_paths]

def binary_tree_paths(root):
	if root is None:
		return []
	elif not any(root.neighbors):
		return [[root.weight]]
	else:
		left_paths = binary_tree_path(root.neighbors[0])
		right_paths = binary_tree_path(root.neighbors[1])
		return [[root.weight] + path for path in left_paths] + [[root.weight] + path for path in right_paths]

def sum_numbers(root):
	if root is None:
		return None
	elif not any(root.neighbors):
		return root.weight
	else:
		left = 




if __name__ == '__main__':
	from ... import random_graph
	root = random_graph.generate_random_binary_tree(10)
	paths = binary_tree_path_sum(root, 30)
	print(paths)
