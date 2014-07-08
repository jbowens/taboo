#!/usr/bin/env python
import sys, json, re, psycopg2

CONN_STR = 'dbname=prod user=prod'
digits = re.compile('\d')

conn = psycopg2.connect(CONN_STR)
conn.autocommit = True
cur = conn.cursor()

def valid_word(word):
    if bool(digits.search(word)):
        # Don't allow digits in any of our words
        return False
    if len(word) < 4:
        # Only want longer words
        return False

    # Make sure the word doesn't already exist.
    cur.execute("SELECT COUNT(word) FROM words WHERE word = %s;", (word,))
    exists = cur.fetchone()[0]
    return not exists

with open('rawdata.txt') as f:
    lines = f.read().lower().splitlines()
    words = dict(filter(lambda y: valid_word(y[0]), zip(lines[::2], map(lambda x: x.split('|')[:20:2], lines[1::2]))))

    for w in words:
        print w + ': ' + ', '.join(words[w])
