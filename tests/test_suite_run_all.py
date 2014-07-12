import unittest
import test_url_graph
import test_url_node

modules = [test_url_graph, test_url_node]

loader = unittest.TestLoader()
for module in modules: 
	unittest.TextTestRunner(verbosity=2).run(loader.loadTestsFromModule(module))
