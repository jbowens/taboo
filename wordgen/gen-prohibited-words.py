import urllib2
import json
import re
from HTMLParser import HTMLParser



===================== NO LONGER NEEDED ======================
* See java folder for the functionality that was handled here.



MAX_CHARS = 40

"""MLStripper strips strings of markup language.
"""

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

stripper = MLStripper()		# hahahaha var name...
f = open('wiki_pop_links.txt', 'r')
content = f.read()
links = json.loads(content)
base_url = 'http://en.wikipedia.org'
junk_len = len('\"wgTitle\":\"')

for link in [links[0]]:
	# get link content
#	print "link: " + link
	page = urllib2.urlopen(base_url+link).read()
	start_idx = page.find('\"wgTitle\":\"')
	offset = start_idx+junk_len
	end_idx = page[offset+1:offset+MAX_CHARS].find('\"')+offset+1
#	print offset
#	print end_idx
	if (end_idx != offset):			# only keep words with title < 40 chars
		name = page[offset:end_idx]
		MLless_page= stripper.feed(page.encode("utf8")).get_data() 	# removes ML
		print MLless_page
	# get unigrams and bigrams
