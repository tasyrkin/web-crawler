import unittest
from main.url_graph import UrlNode

class UrlNodeTest(unittest.TestCase):

	def testGetName(self):
		node = UrlNode('test_name')
		self.assertEquals('test_name', node.get_name())

if __name__ == '__main__':
	unittest.main()
