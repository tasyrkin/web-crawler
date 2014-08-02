import unittest
from webcrawler.url_graph import UrlGraph
from webcrawler.url_graph import UrlNode

NODE_URL_STR1 = u'http://www.google.com'
NODE_URL_STR2 = u'http://www.amazon.com'
NODE_URL_STR3 = u'http://www.microsoft.com'

class UrlGraphTest(unittest.TestCase):

	def test_add_connection(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)

		self.assertEquals(UrlNode(NODE_URL_STR1), graph.get_node(NODE_URL_STR1))
		self.assertEquals(UrlNode(NODE_URL_STR2), graph.get_node(NODE_URL_STR2))

	def test_get_node(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)

		node1 = graph.get_node(NODE_URL_STR1)
		node2 = graph.get_node(NODE_URL_STR2)

		self.assertTrue(node2 in node1.get_nodes())
		self.assertTrue(node1 not in node2.get_nodes())

	def test_add_connection_several_nodes(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)
		graph.add_connection(NODE_URL_STR1, NODE_URL_STR3)
		graph.add_connection(NODE_URL_STR2, NODE_URL_STR3)

		self.assertEquals(2, len(graph.get_node(NODE_URL_STR1).get_nodes()))
		self.assertEquals(1, len(graph.get_node(NODE_URL_STR2).get_nodes()))
		self.assertEquals(0, len(graph.get_node(NODE_URL_STR3).get_nodes()))

	def test_add_connection_same_node(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL_STR1, NODE_URL_STR1)

		self.assertTrue(graph.get_node(NODE_URL_STR1) is None)

	def test_add_node(self):
		graph = UrlGraph()

		graph.add_node(NODE_URL_STR1)

		self.assertEquals(UrlNode(NODE_URL_STR1), graph.get_node(NODE_URL_STR1))

	def test_get_nodes(self):
		graph = UrlGraph()

		graph.add_node(NODE_URL_STR1)
		graph.add_node(NODE_URL_STR2)

		expected_nodes = [graph.get_node(NODE_URL_STR1), graph.get_node(NODE_URL_STR2)]

		self.assertSetEqual(set(graph.get_nodes()), set(expected_nodes))

	def test__str__(self):
		graph = UrlGraph()

		graph.add_node(NODE_URL_STR1)
		graph.add_node(NODE_URL_STR2)
		graph.add_connection(NODE_URL_STR1, NODE_URL_STR2)

		print graph

if __name__ == '__main__':
	unittest.main()
