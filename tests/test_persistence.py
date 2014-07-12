import unittest
from webcrawler.url_graph import UrlGraph
from webcrawler.persistence import UrlGraphFileLoader
from webcrawler.persistence import UrlGraphFilePersister

NODE_URL_STR1 = 'http://www.google.com'
NODE_URL_STR2 = 'http://www.amazon.com'
NODE_URL_STR3 = 'http://www.microsoft.com'

class PersistenceTest(unittest.TestCase):

	def test_add_connection(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)
		graph.add_connection(NODE_URL_STR1, NODE_URL_STR3)
		graph.add_connection(NODE_URL_STR2, NODE_URL_STR3)

		UrlGraphFilePersister().persist('test_file_name.txt', graph)
		loaded_graph = UrlGraphFileLoader().load('test_file_name.txt')

		expected_nodes = [graph.get_node(NODE_URL_STR1), graph.get_node(NODE_URL_STR2), graph.get_node(NODE_URL_STR3)]

		self.assertSetEqual(set(loaded_graph.get_nodes()), set(expected_nodes), 'persisted graph')

