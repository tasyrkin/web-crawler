import os
import fileinput

class UrlNode:
	'''
	Represents a url as a node of a url graph
	'''
	def __init__(self, url):
		self._url = url
		self._nodes = set()

	def get_url(self):
		return self._url

	def add_node(self, url_node):
		self._nodes.add(url_node)

	def get_nodes(self):
		return self._nodes

	def _get_neighbour_urls(self):
		return map(lambda node: node.get_url(), self._nodes)
	
	@staticmethod
	def _truncate_list_for_string(lst, limit):
		return str(lst[0:limit]) + (', ...' if len(lst)>limit else '')

	def __str__(self):
		neighbour_urls = self._get_neighbour_urls()
		return self._url + '->' + UrlNode._truncate_list_for_string(neighbour_urls, 10)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		if not isinstance(other, UrlNode):
			return False
		return self._url == other._url

	def __hash__(self):
		return hash(self._url)

class UrlGraph:
	'''
	Represents a graph of url nodes
	'''
	def __init__(self):
		self._nodes = dict()

	def _add_if_not_exists_and_get_node(self, node_url):
		node = self._nodes.get(node_url)
		if node is None:
			node = UrlNode(node_url)
			self._nodes[node_url] = node
		return node

	def add_connection(self, node_url1, node_url2):

		assert isinstance(node_url1, str) and node_url1.strip() != '', 'Expected non empty url, but was {}'.format(node_url1)
		assert isinstance(node_url2, str) and node_url2.strip() != '', 'Expected non empty url, but was {}'.format(node_url2)

		node1 = self._add_if_not_exists_and_get_node(node_url1)
		node2 = self._add_if_not_exists_and_get_node(node_url2)

		node1.add_node(node2)
		node2.add_node(node1)

	def get_node(self, node_url):
		return self._nodes.get(node_url)

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

