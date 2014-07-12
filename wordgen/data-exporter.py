#!/usr/bin/env python
import sys, json, psycopg2, argparse

parser = argparse.ArgumentParser(description='Exports word data from the database to a json file.')
parser.add_argument('--verified-only', dest='verified', action='store_true', help='if provided, only verified words will be exported')
args = parser.parse_args()

CONN_STR = 'dbname=prod user=prod'

conn = psycopg2.connect(CONN_STR)

cur = conn.cursor()

if args.verified:
    cur.execute("SELECT id, word FROM words WHERE verified")
else:
    cur.execute("SELECT id, word FROM words")

words = [];

rows = cur.fetchall()
for row in rows:
    w = dict()
    w['id'] = row[0]
    w['word'] = row[1]

    cur.execute("SELECT word FROM prohibited_words WHERE wordid = " + str(row[0]) + " ORDER BY rank ASC")
    prohibited_words = map(lambda x: x[0], cur.fetchall())

    w['prohibited'] = prohibited_words
    words.append(w);

conn.commit()
cur.close()
conn.close()

print json.dumps(words)
