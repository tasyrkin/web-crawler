import logging
import logging.config

logging.config.fileConfig('../resources/logging.conf')
logger = logging.getLogger(__name__)

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

	def _add_if_not_exists_and_get_node(self, url_node_str):
		node = self._nodes.get(url_node_str)
		if node is None:
			node = UrlNode(url_node_str)
			self._nodes[url_node_str] = node
		return node

	def add_node(self, url_node_str):
		return self._add_if_not_exists_and_get_node(url_node_str)

	def add_connection(self, url_str_from, url_str_to):

		assert isinstance(url_str_from, str) and url_str_from.strip() != '', 'Expected non empty url, but was {}'.format(url_str_from)
		assert isinstance(url_str_to, str) and url_str_to.strip() != '', 'Expected non empty url, but was {}'.format(url_str_to)

		url_str_from = url_str_from.strip()
		url_str_to = url_str_to.strip()
		
		if url_str_from == url_str_to:
			logger.warn('Attemption to connect the url [{}] to itself is ignored'.format(url_str_from))
			return

		node1 = self._add_if_not_exists_and_get_node(url_str_from)
		node2 = self._add_if_not_exists_and_get_node(url_str_to)

		node1.add_node(node2)

	def get_node(self, node_url_str):
		return self._nodes.get(node_url_str)
	
	def get_nodes(self):
		return self._nodes.values()
	
	def __str__(self):
		nodes = self.get_nodes()
		return '\n'.join(map(lambda node: str(node), nodes))