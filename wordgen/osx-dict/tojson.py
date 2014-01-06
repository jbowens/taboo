#!/usr/bin/env python
import sys, json

words = dict()
for line in sys.stdin:
    pieces = line.split(':')
    prohibited = map(lambda x: x.strip(), pieces[1].split(', '))
    words[pieces[0]] = prohibited

print json.dumps(words)
