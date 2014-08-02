import unittest

from webcrawler.crawler_utils import HopsCounter

class HopsCounterTest(unittest.TestCase):

	def test_hops_counter_finite(self):

		hops_counter = HopsCounter(1)

		self.assertTrue(hops_counter.can_hop())

		hops_counter.hop()

		self.assertFalse(hops_counter.can_hop())

	def test_hop_counter_infinite(self):

		hops_counter = HopsCounter(0)

		self.assertTrue(hops_counter.can_hop())

		for _ in range(100):
			hops_counter.hop()

		self.assertTrue(hops_counter.can_hop())
