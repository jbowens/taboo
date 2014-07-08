#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, json, re, psycopg2, DictionaryServices

CONN_STR = 'dbname=prod user=prod'
digits = re.compile('\d')

conn = psycopg2.connect(CONN_STR)
conn.autocommit = True
cur = conn.cursor()

prohibited_pos = ['pronoun', 'preposition', 'prefix', 'abbreviation',
                  'exclamation', 'adverb', 'det.', 'cardinal', 'exclam.',
                  'ordinal', 'poss.', 'interrog.', 'predet.', 'preposition,',
                  'rel.', 'modal', 'contr.']

def get_pos(word):
    text = DictionaryServices.DCSCopyTextDefinition(None, word, (0, len(word)))
    if not text or len(text) == 0:
        return None
    text = unicode(text)
    pieces = text.split(u'▶')
    if len(pieces) < 2:
        return None
    pos = pieces[1].split()[0]
    return pos

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
    if exists:
        return False

    pos = get_pos(word)
    if pos in prohibited_pos:
        return False

    return True

with open('rawdata.txt') as f:
    lines = f.read().lower().splitlines()
    words = dict(filter(lambda y: valid_word(y[0]), zip(lines[::2], map(lambda x: x.split('|')[:20:2], lines[1::2]))))

    for w in words:
        print w + ': ' + ', '.join(words[w])
