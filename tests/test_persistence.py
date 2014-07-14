import unittest
from webcrawler.url_graph import UrlGraph
from webcrawler.persistence import UrlGraphFileLoader
from webcrawler.persistence import UrlGraphFilePersister
from webcrawler.persistence import PersistenceManager
import datetime

NODE_URL_STR1 = 'http://www.google.com'
NODE_URL_STR2 = 'http://www.amazon.com'
NODE_URL_STR3 = 'http://www.microsoft.com'
TEST_FILE_NAME = 'test_file_to_ignore.txt'

class PersistenceTest(unittest.TestCase):

	def test_persist_and_load(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)
		graph.add_connection(NODE_URL_STR1, NODE_URL_STR3)
		graph.add_connection(NODE_URL_STR2, NODE_URL_STR3)

		UrlGraphFilePersister().persist(TEST_FILE_NAME, graph)
		loaded_graph = UrlGraphFileLoader().load(TEST_FILE_NAME)

		expected_nodes = [graph.get_node(NODE_URL_STR1), graph.get_node(NODE_URL_STR2), graph.get_node(NODE_URL_STR3)]

		self.assertSetEqual(set(loaded_graph.get_nodes()), set(expected_nodes), 'persisted graph')

	def test_persistence_manager(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)
		graph.add_connection(NODE_URL_STR1, NODE_URL_STR3)
		graph.add_connection(NODE_URL_STR2, NODE_URL_STR3)

		now = datetime.datetime.now()

		manager = PersistenceManager(graph)
		manager._run_cycle(now)

		graph_file_path = manager._get_persistence_file_path(now, 1)

		loaded_graph = UrlGraphFileLoader().load(graph_file_path)

		expected_nodes = [graph.get_node(NODE_URL_STR1), graph.get_node(NODE_URL_STR2), graph.get_node(NODE_URL_STR3)]

		self.assertSetEqual(set(loaded_graph.get_nodes()), set(expected_nodes), 'graph persisted with manager')