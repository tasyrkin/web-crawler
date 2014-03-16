import os
import fileinput

class UrlNode:

	def __init__(self, name):
		self.name = name
		self.urls = list()

	def add_url_node(self, url_node):
		self.urls.append(url)
	
	def add_url_nodes(self, url_nodes):
		self.urls.extend(urls)

class UrlGraph:
	init_url_node = None

	def __init__(self, url_node):
		pass

	def __init__(self, url_node):
		self.init_url_node = url_node

	def find_url_node_by_name(self, url_node):
		except NotImplementedError()

class UrlGraphFileSystemPersister:
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
			except ValueError(str.format('found multiple url graph files: {}', str(url_graph_fnames)))
		
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
		except NotImplementedError()

