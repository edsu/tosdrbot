#!/usr/bin/env python3

"""
Convert terms of service documents monitored by the tosdr.org into RSS
for use with diffengine.
"""

import re
import html
import requests


def service_names():
    html = requests.get('https://github.com/tosdr/tosdr.org/tree/master/api/1/service').text
    yield from re.findall('<a.+? title="(.+)\.json">', html)


def links(service_name):
    service_url = 'https://tosdr.org/api/1/service/%s.json' % service_name
    service = requests.get(service_url).json()
    for key, link in service['links'].items():
        title = '%s: %s' % (service_name.capitalize(), link['name'])
        yield {'url': link['url'], 'title': title}


def item(link):
    return """<item><title>%(title)s</title><link>%(url)s</link><guid>%(url)s</guid><description>%(title)s</description></item>""" % {'title': html.escape(link['title']), 'url': html.escape(link['url'])}


def main():
    print("""<?xml version="1.0" encoding="utf-8" ?><rss version="2.0" xml:base="https://tosdr.org/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Terms of Service Didn't Read - Service Links</title><link>https://tosdr.org/</link><description>Links to Terms of Service documents managed by the ToSDR service</description><language>en</language><atom:link href="https://inkdroid.org/rss/tosdr.xml" rel="self" type="application/rss+xml" />""", end="") 

    for service_name in service_names():
        for link in links(service_name):
            print(item(link))

    print("</channel></rss>", end="")


if __name__ == '__main__':
    main()

