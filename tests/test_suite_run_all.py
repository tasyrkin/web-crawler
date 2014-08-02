import unittest
import test_url_graph
import test_url_node
import test_persistence
import test_hop_counter

modules = [test_url_graph, test_url_node, test_persistence, test_hop_counter]

loader = unittest.TestLoader()
for module in modules: 
	unittest.TextTestRunner(verbosity=2).run(loader.loadTestsFromModule(module))
