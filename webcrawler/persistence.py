import url_graph

class UrlGraphFilePersister:

	def persist(self, file_name, url_graph):
		with open(file_name, 'w') as f:
			for url_node in url_graph.get_nodes():
				neighbours = ",".join(map(lambda node: node.get_url(), url_node.get_nodes()))
				f.write("{}->{}\n".format(url_node.get_url(),neighbours))


class UrlGraphFileLoader:

	def load(self, file_name):
		graph = url_graph.UrlGraph()

		with open(file_name, 'r') as f:
			for line in f.readlines():
				head_and_neighbours = line.split('->', 1)
				assert len(head_and_neighbours) == 2, 'Unexpected url node persisted format, found [{}]'.format(head_and_neighbours)
				head_node = head_and_neighbours[0].strip()
				for neighbour in [neighbour.strip() for neighbour in head_and_neighbours[1].split(',') if neighbour.strip()!='']:
					graph.add_connection(head_node, neighbour)
			return graph
