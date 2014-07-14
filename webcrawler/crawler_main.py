import urlparse
import sys
import httplib
from lxml import etree
from crawler_params import ParamsManager
from url_graph import UrlGraph
import time

def get_prefixed_string_or_empty(string, prefix):
	return prefix + string if string != '' else '' 

def fetch_urls(parsed_url):

	try:
		conn = httplib.HTTPConnection(parsed_url.netloc)
		conn.request("GET", parsed_url.path + get_prefixed_string_or_empty(parsed_url.query, '?') + get_prefixed_string_or_empty(parsed_url.fragment, '#'))
		resp = conn.getresponse()
		content_type = resp.getheader("content-type")
		data = resp.read()
	except Exception, e:
		print 'Unable to fetch data from [{}], error [{}]'.format(parsed_url.geturl(), str(e))
		return []

	if 'text/html' not in content_type.split(';'):
		print 'Fetched content type [{}] is skipped'.format(content_type)
		return []

	try:
		html_dom = etree.HTML(data)
	except Exception, e:
		print 'Unable to parse data from [{}], error [{}]'.format(parsed_url.geturl(), str(e))
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

def traverse_web_graph(start_url):

	graph = UrlGraph()

	parsed_url = urlparse.urlparse(start_url)
	graph.add_node(parsed_url.geturl())

	parsed_urls_queue = [parsed_url]
	visited_urls = set()

	while len(parsed_urls_queue) > 0:
		parsed_url = parsed_urls_queue.pop(0)

		if parsed_url.geturl() in visited_urls:
			print ('[{}] already visited...skipping...'.format(parsed_url.geturl()))
			continue
		visited_urls.add(parsed_url.geturl())
		graph.add_node(parsed_url.geturl())

		parsed_fetched_urls = fetch_urls(parsed_url)
		parsed_urls_queue.extend(filter(lambda url: url.geturl() not in visited_urls, parsed_fetched_urls))

		print 'for url {} fetched urls {}'.format(parsed_url.geturl(), str(map(lambda parsed_url: parsed_url.geturl(), parsed_fetched_urls)))

		for parsed_fetched_url in parsed_fetched_urls:
			graph.add_connection(parsed_url.geturl(), parsed_fetched_url.geturl())

		time.sleep(10)

params_manager = ParamsManager(sys.argv)

traverse_web_graph(params_manager.get(ParamsManager.PARAM_INIT_URL))
