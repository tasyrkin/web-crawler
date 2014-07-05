import unittest
from main.url_graph import UrlNode

NODE_NAME1 = 'test_name1'
NODE_NAME2 = 'test_name2'

class UrlNodeTest(unittest.TestCase):


	def test_get_name(self):
		node = UrlNode(NODE_NAME1)
		self.assertEquals(NODE_NAME1, node.get_name())

	def test_get_nodes(self):
		node1 = UrlNode(NODE_NAME1)
		node2 = UrlNode(NODE_NAME2)
		node1.add_node(node2)

		self.assertEquals(node2, list(node1.get_nodes())[0])

if __name__ == '__main__':
	unittest.main()
