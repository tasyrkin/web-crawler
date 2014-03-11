from __future__ import print_function
import urlparse
import util.url_util
import util.storage_util
import sys
from lxml import etree
__author__ = 'tasyrkin'

def traverse_web_graph(start_url):

	start_url_parsed = urlparse.urlparse(start_url)
    
	#visited_urls = util.storage_util.restore_set(start_url_parsed.netloc)
	visited_urls = set()
	queue = []

	queue.append(start_url)

	total_urls_count = 0
	skipped_urls_count = 0
	error_urls_count = 0
	while len(queue) > 0:
		url = queue.pop(0)

		print (str.format('processed: [{}], skipped: [{}], error: [{}], processing url: [{}]', total_urls_count, skipped_urls_count, error_urls_count, url))

		if url in visited_urls:
			print ('already visited...skipping...')
			skipped_urls_count = skipped_urls_count + 1
			continue

		visited_urls.add(url)

		try:
			html_dom = etree.HTML(util.url_util.readUrlAsString(url))
		except Exception:
			error_urls_count = error_urls_count + 1
			continue
		
		links = html_dom.xpath('//a')

		cnt = 0
		for sub_link in links:
			for key in sub_link.keys():
				if key == 'href':
					sub_url = sub_link.get(key)
					parsed_sub_url = urlparse.urlparse(sub_url)
					if not parsed_sub_url.scheme:
						sub_url = urlparse.urljoin(url, sub_url)
					else:
						if parsed_sub_url.scheme == 'javascript':
							continue
					queue.append(sub_url)
					#print('link [{0}]: {1}'.format(cnt, sub_url), end=' ')
					cnt += 1
					total_urls_count = total_urls_count + 1

					print ('found links [{0}]'.format(cnt))

if __name__ == '__main__':

	print ('Entering main......')

	if len(sys.argv) != 2:
		raise ValueError("start url must be provided")

	start_url = sys.argv[1]

	traverse_web_graph(start_url)
