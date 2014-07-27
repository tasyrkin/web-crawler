import urlparse
import sys
import httplib
from lxml import etree
import threading
import logging

from crawler_params import ParamsManager
from url_graph import UrlGraph
from persistence import UrlGraphFileLoader
from persistence import PersistenceManager

logging.config.fileConfig('../resources/logging.conf')
logger = logging.getLogger(__name__)

CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'UTF-8'

def get_prefixed_string_or_empty(string, prefix):
	return prefix + string if string != '' else ''


def parse_content_type_and_charset(header_content_type):
	assert header_content_type is not None, 'header_content_type is missing'

	content_type_and_charset = map(lambda element: element.strip(), header_content_type.split(';'))

	charset = DEFAULT_CHARSET
	if len(content_type_and_charset) == 1:
		return content_type_and_charset[0], charset
	if len(content_type_and_charset) >= 2:
		charset_and_encoding = content_type_and_charset[1]
		if '=' in charset_and_encoding:
			charset_and_encoding_list = charset_and_encoding.split('=')
			if len(charset_and_encoding_list) == 2:
				charset = charset_and_encoding_list[1].strip()
		return content_type_and_charset[0], charset


def fetching_stopped_because_no_http_content_type(string_url, header_content_type):
	if header_content_type is None:
		logger.warn('Fetched content type [{}] is skipped, url: [{}]'.format(header_content_type, string_url))
		return True
	return False

def fetching_stopped_because_no_content_type_or_charset(string_url, content_type, charset):
	if len(content_type) == 0 or len(charset) == 0:
		print 'Fetched content type [{}] or encoding [{}] is empty, url: [{}]'.format(content_type, charset, string_url)
		return True
	return False

def fetching_stopped_because_unsupported_content_type(string_url, content_type):
	if 'text/html' != content_type:
		print 'Fetched content type [{}] is skipped, url: [{}]'.format(content_type, string_url)
		return True
	return False

def fetch_urls(parsed_url):

	try:
		conn = httplib.HTTPConnection(parsed_url.netloc)
		conn.request("GET", parsed_url.geturl())
		resp = conn.getresponse()
		header_content_type = resp.getheader("content-type")
		data = resp.read()
	except Exception, e:
		print 'Unable to fetch data from [{}], error [{}]'.format(parsed_url.geturl(), str(e))
		return []

	if fetching_stopped_because_no_http_content_type(parsed_url.geturl(), header_content_type):
		return []

	content_type, charset = parse_content_type_and_charset(header_content_type)

	if fetching_stopped_because_no_content_type_or_charset(parsed_url.geturl(), content_type, charset):
		return []

	try:
		html_dom = etree.HTML(data.decode(charset))
	except Exception, e:
		print 'Unable to parse data, error [{}], url: [{}]'.format(str(e), parsed_url.geturl())
		return []

	found_url_elements = html_dom.xpath('//a')

	parsed_found_urls = []
	for url_element in found_url_elements:
		for key in url_element.keys():
			if key == 'href':
				href = url_element.get(key)
				parsed_href = urlparse.urlparse(href)
				if not parsed_href.scheme:
					joined_href = urlparse.urljoin(parsed_url.geturl(), href)
					parsed_href = urlparse.urlparse(joined_href)
				parsed_found_urls.append(parsed_href)

	return parsed_found_urls

def traverse_url_graph(url_graph):

	start_urls = map(lambda node: node.get_url(), url_graph.get_nodes_without_neighbours())

	print start_urls

	parsed_urls_stack = map(lambda url: urlparse.urlparse(url), start_urls)
	visited_urls = set()

	while len(parsed_urls_stack) > 0:
		parsed_url = parsed_urls_stack.pop()

		if parsed_url.geturl() in visited_urls:
			print ('[{}] already visited...skipping...'.format(parsed_url.geturl()))
			continue
		visited_urls.add(parsed_url.geturl())
		url_graph.add_node(parsed_url.geturl())

		parsed_fetched_urls = fetch_urls(parsed_url)
		parsed_urls_stack.extend(filter(lambda url: url.geturl() not in visited_urls, parsed_fetched_urls))

		print 'for url {} fetched urls {}'.format(parsed_url.geturl(), str(map(lambda parsed_url: parsed_url.geturl(), parsed_fetched_urls)))

		for parsed_fetched_url in parsed_fetched_urls:
			url_graph.add_connection(parsed_url.geturl(), parsed_fetched_url.geturl())

def persist_url_graph(url_graph):
	PersistenceManager(url_graph).run()

if __name__ == '__main__':
	params_manager = ParamsManager(sys.argv)

	graph = UrlGraph()
	if params_manager.has_value(ParamsManager.PARAM_URL_GRAPH_FILE_PATH):
		graph = UrlGraphFileLoader().load(params_manager.get_value(ParamsManager.PARAM_URL_GRAPH_FILE_PATH)) 

	graph.add_node(params_manager.get_value(ParamsManager.PARAM_INIT_URL))

	th = threading.Thread(target=persist_url_graph, args=(graph,))
	th.start()

	traverse_url_graph(graph)

	th.join()
