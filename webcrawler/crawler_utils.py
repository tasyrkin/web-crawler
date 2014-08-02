
class HopsCounter:
	INFINITE = 0

	def __init__(self, hops_limit):

		assert hops_limit >= HopsCounter.INFINITE, 'Expected non negative value, but was [{}]'.format(hops_limit)

		self.__hops_limit = hops_limit
		self.__is_infinite = self.__hops_limit == HopsCounter.INFINITE
		self.__hops_done = 0

	def can_hop(self):
		return self.__is_infinite or self.__hops_limit > self.__hops_done

	def hop(self):

		assert self.can_hop(), 'Expected to be able to hop, but was not {}'.format(str(self))

		self.__hops_done += 1

	def __str__(self):
		return 'hops_limit = {}, hops_done = {}, is_infinite = {}'.format(self.__hops_limit, self.__hops_done, self.__is_infinite)