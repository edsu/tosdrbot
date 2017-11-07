#!/usr/bin/env python3

"""
Convert terms of service documents monitored by the tosdr.org into RSS
for use with diffengine.
"""

import io
import re
import html
import logging
import zipfile
import tempfile

from xml.etree import ElementTree
from urllib.request import urlretrieve

def get_links():
    url = 'https://github.com/tosdr/tosback2/archive/master.zip'
    tmp = tempfile.NamedTemporaryFile()
    urlretrieve(url, tmp.name)
    tosdr = zipfile.ZipFile(tmp.name)
    for info in tosdr.infolist():
        if re.search('/rules/.*\.xml', info.filename):
            try:
                root = ElementTree.parse(tosdr.open(info)).getroot()
                site = root.attrib['name']
                for doc in root.findall('docname'):
                    url = doc.find('url')
                    yield {
                        'title': '%s - %s' % (site, doc.attrib['name']),
                        'url': url.attrib['name']
                    }
            except Exception as e:
                logging.error('error when parsing %s: %s', info.filename, e)

def item(link):
    return """<item><title>%(title)s</title><link>%(url)s</link><guid>%(url)s</guid><description>%(title)s</description></item>""" % {'title': html.escape(link['title']), 'url': html.escape(link['url'])}


def main():
    print("""<?xml version="1.0" encoding="utf-8" ?><rss version="2.0" xml:base="https://tosdr.org/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Terms of Service Didn't Read - Service Links</title><link>https://tosdr.org/</link><description>Links to Terms of Service documents managed by the ToSDR service</description><language>en</language><atom:link href="https://inkdroid.org/rss/tosdr.xml" rel="self" type="application/rss+xml" />""", end="") 

    for link in get_links():
        print(item(link))

    print("</channel></rss>", end="")


if __name__ == '__main__':
    logging.basicConfig(filename='rss.log', level=logging.INFO)
    main()

