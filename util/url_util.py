import urllib
__author__ = 'tasyrkin'


def readUrlAsString(url):
    filehandle = urllib.urlopen(url)

    try:
        url_lines = filehandle.readlines()
        document_content = ''

        for line in url_lines:
            document_content += line
        
        return document_content

    except:
        return ''
