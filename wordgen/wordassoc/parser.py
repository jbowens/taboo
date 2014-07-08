#!/usr/bin/env python
import sys, json, re

digits = re.compile('\d')

def valid_word(word):
    if bool(digits.search(word)):
        # Don't allow digits in any of our words
        return False
    if len(word) < 4:
        # Only want longer words
        return False
    return True

with open('rawdata.txt') as f:
    lines = f.read().lower().splitlines()
    words = dict(filter(lambda y: valid_word(y[0]), zip(lines[::2], map(lambda x: x.split('|')[:20:2], lines[1::2]))))
    for w in words:
        print w
