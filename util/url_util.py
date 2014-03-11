import urllib
__author__ = 'tasyrkin'


def readUrlAsString(url):

	try:
		filehandle = urllib.urlopen(url)
		url_lines = filehandle.readlines()
		document_content = ''
		for line in url_lines:
			document_content += line
		return document_content
	except Exception:
		return ''
