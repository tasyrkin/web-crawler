from __future__ import print_function
import urlparse
import util.url_util
from lxml import etree
__author__ = 'tasyrkin'

def construct_url(parsed_url, path):
    return parsed_url.scheme + '://' + parsed_url.netloc + path 

#start_url = sys.args[0]
start_url = 'http://google.com'

link_counts = {}
visited_urls = set()
queue = []

queue.append(start_url)

while len(queue) > 0:

    url = queue.pop(0)
    
    parsed_url = urlparse.urlparse(url)

    print ('elaborating [{0}]'.format(url), end=' ')

    #TODO: exclude javascript urls
    
    if url in visited_urls:
        print ('already visited...skipping...')
        continue

    visited_urls.add(url)

    html_dom = etree.HTML(util.url_util.readUrlAsString(url))

    links = html_dom.xpath('//a')

    cnt = 0
    for sub_link in links:
        for key in sub_link.keys():
            if key == 'href':
                sub_url = sub_link.get(key)
                if sub_url.startswith('/'):
                    sub_url = construct_url(parsed_url, sub_url)
                queue.append(sub_url)
                #print('link [{0}]: {1}'.format(cnt, sub_url), end=' ')

                cnt += 1

    print ('found links [{0}]'.format(cnt))
