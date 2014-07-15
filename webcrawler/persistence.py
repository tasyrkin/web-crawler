import url_graph
import datetime
import time
import logging
import os

logging.config.fileConfig('../resources/logging.conf')
logger = logging.getLogger(__name__)

_NEIGHBOURS_SEPARATOR = ','
_CONNECTIONS_SEPARATOR = '->'

class UrlGraphFilePersister:

	def persist(self, file_name, url_graph):
		with open(file_name, 'w') as f:
			for url_node in url_graph.get_nodes():
				neighbours = _NEIGHBOURS_SEPARATOR.join(map(lambda node: node.get_url(), url_node.get_nodes()))
				f.write("{}{}{}\n".format(url_node.get_url(), _CONNECTIONS_SEPARATOR, neighbours))


class UrlGraphFileLoader:

	def load(self, file_name):
		graph = url_graph.UrlGraph()

		with open(file_name, 'r') as f:
			for line in f.readlines():
				head_and_neighbours = line.split(_CONNECTIONS_SEPARATOR, 1)
				assert len(head_and_neighbours) == 2, 'Unexpected url node persisted format, found [{}]'.format(head_and_neighbours)
				head_node = head_and_neighbours[0].strip()
				for neighbour in [neighbour.strip() for neighbour in head_and_neighbours[1].split(_NEIGHBOURS_SEPARATOR) if neighbour.strip()!='']:
					graph.add_connection(head_node, neighbour)
			return graph

class PersistenceManager:
	TIME_PERIOD_IN_SECONDS = 10
	STORAGE_DIRECTORY = '../storage'
	PERSISTENCE_FILE_TEMPLATE = 'url_graph_{}.version_{}'
	
	def __init__(self, url_graph):
		self._url_graph = url_graph
		self._version = 1
		self._persister = UrlGraphFilePersister()
	
	def _get_persistence_file_path(self, datetime_now, version):
		datetime_format = datetime_now.strftime('%Y-%m-%d_%H-%M-%S_%f')
		file_name = PersistenceManager.PERSISTENCE_FILE_TEMPLATE.format(datetime_format, version) 
		return os.path.join(PersistenceManager.STORAGE_DIRECTORY, file_name)

	def _run_cycle(self, datetime_now):
		file_path = self._get_persistence_file_path(datetime_now, self._version)
		self._persister.persist(file_path, self._url_graph)
		logger.debug('Persisted url graph, version {}'.format(self._version))
		self._version += 1

	def run(self):
		while True:
			try:
				time.sleep(PersistenceManager.TIME_PERIOD_IN_SECONDS)
				self._run_cycle(datetime.datetime.now())
			except Exception, e:
				logger.error('Unable to persist graph, error [{}]'.format(str(e)))
