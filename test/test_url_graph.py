import unittest
from main.url_graph import UrlGraph
from main.url_graph import UrlNode

NODE_URL1 = 'http://www.google.com'
NODE_URL2 = 'http://www.amazon.com'

class UrlGraphTest(unittest.TestCase):

	def test_add_connection(self):
		graph = UrlGraph()

		graph.add_connection(NODE_URL1, NODE_URL2)

		self.assertEquals(UrlNode(NODE_URL1), graph.get_node(NODE_URL1))
		self.assertEquals(UrlNode(NODE_URL2), graph.get_node(NODE_URL2))

if __name__ == '__main__':
	unittest.main()
