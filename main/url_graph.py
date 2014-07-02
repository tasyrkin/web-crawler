import os
import fileinput

class UrlNode:
	'''
	Represents a url as a node of a graph
	'''
	def __init__(self, name):
		self._name = name
		self._nodes = set()

	def add_node(self, url_node):
		self._nodes.add(url_node)

	def get_name(self):
		return self._name

	def __str__(self):
		nlen = len(self._nodes)
		return self._name + '->' + str(nlen if nlen > 5 else map(lambda node: node.get_name(), self._nodes))

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		if not isinstance(other, UrlNode):
			return False
		return self._name == other._name

class UrlGraph:
	'''
	Represents a graph of url nodes
	'''
	def __init__(self):
		self._nodes = dict()

	def add_connection(self, node_url1, node_url2):

		assert isinstance(node_url1, str) and node_url1.strip() != '', 'Expected non empty string, but was {}'.format(node_url1)
		assert isinstance(node_url2, str) and node_url2.strip() != '', 'Expected non empty string, but was {}'.format(node_url2)

		node1 = self._map.get(node_name1)
		if node1 is None:
			node1 = UrlNode(node_url1)
			self._map[node_url1] = node1

		node2 = self._map.get(node_url2)
		if node2 is None:
			node2 = UrlNode(node_url2)
			self._map[node_url2] = node2

		node1.add_node(node2)
		node2.add_node(node1)

	def find_url_node(self, node_name):
		raise NotImplementedError()

class FilePersister:
	NAME_PATTERN_URL_GRAPH = 'url_graph_'

	def __init__(self, folder):
		self.folder = folder
	
	def load_url_graph(self):
		url_graph_fnames = [fname 
				for fname in os.listdir(folder) 
				if fname.startswith(NAME_PATTERN_URL_GRAPH)]
		if len(url_graph_fnames) == 0:
			return UrlGraph()
		if len(url_graph_fnames) > 1:
			raise ValueError(str.format('found multiple url graph files: {}', str(url_graph_fnames)))
		
		str_to_url_node = dict()
		init_node = None
		for line in fileinput(url_graph_fnames[0]):
			url_to_neighbours = line.split(':')
			url_str = url_to_neighbours[0]
			neighbours_str = url_to_neighbours[1].split(',')
			url_node = str_to_url_node.get(url_str)
			if not url_node:
				url_node = UrlNode(url_str)
				str_to_url_node[url_str] = url_node
			for neighbour_str in neighbours_str:
				neighbour_node = str_to_url_node.get(neigbour_str)
				if not neighbour_node:
					neighbour_node = UrlNode(neighbour_str)
					str_to_url_node[neighbour_str] = neighbour_node
				url_node.add_url_node(neighbour_node)
			if not init_node:
				init_node = url_node

		return url_graph(init_node)

	def save_url_graph(self, url_graph):
		raise NotImplementedError()

