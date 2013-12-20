import urllib2
from HTMLParser import HTMLParser
import json

"""Script to grab links to the most popular wikipedia 
pages from the past 7 day period. Outputs all links
as a json array to file 'wiki_pop_links.txt'
"""

class LinkParser(HTMLParser):
	"""Parses for links in HTML tags.
	"""
	def __init__(self, output_list=None):
		HTMLParser.__init__(self)
		if output_list is None:
			self.output_list = []
		else:
			self.output_list = output_list

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			self.output_list.append(dict(attrs).get('href'))


target_url = 'http://en.wikipedia.org/wiki/User:West.andrew.g/Popular_pages'

data = urllib2.urlopen(target_url)
print 'reading data from wikipedia popular pages'
data_str = data.read()
print "length of data string: " + str(len(data_str))
print "using linkparser"
p = LinkParser()
p.feed(data_str)
print "list of links length: " + str(len(p.output_list))
print "first 10 links: "
print p.output_list[:10]

filter_list = [elem for elem in p.output_list if isinstance(elem, basestring)]
filter_list = [elem for elem in filter_list if ':' not in elem]
fine_filter_list = [elem for elem in filter_list if elem[:6] == '/wiki/']

links = json.dumps(fine_filter_list)

f = open('wiki_pop_links.txt', 'w')
f.write(links)
f.close()