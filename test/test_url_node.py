import unittest
from main.url_graph import UrlNode

NODE_URL_STR1 = 'http://www.google.com'
NODE_URL_STR2 = 'http://www.amazon.com'
NODE_URL_STR3 = 'http://www.microsoft.com'
NODE_URL_TEMPLATE_STR = 'http://www.google.com/{}'

class UrlNodeTest(unittest.TestCase):


	def test_get_url(self):
		node = UrlNode(NODE_URL_STR1)
		self.assertEquals(NODE_URL_STR1, node.get_url())

	def test_get_nodes(self):
		node1 = UrlNode(NODE_URL_STR1)
		node2 = UrlNode(NODE_URL_STR2)
		node1.add_node(node2)

		self.assertEquals(node2, list(node1.get_nodes())[0])

	def test_str(self):
		node1 = UrlNode(NODE_URL_STR1)
		for val in range(20):
			node = UrlNode(NODE_URL_TEMPLATE_STR.format(val))
			node1.add_node(node)
		print node1

if __name__ == '__main__':
	unittest.main()
