#!/usr/bin/env python
import sys, json, psycopg2, argparse

parser = argparse.ArgumentParser(description='Imports word data into the taboo database.')
parser.add_argument('--verified', dest='verified', action='store_true', help='include if these words are verified as good quality')
parser.add_argument('--source', dest='source',  help='include to set the source of these imported words')
args = parser.parse_args()

CONN_STR = 'dbname=prod user=prod'

data_str = '\n'.join(sys.stdin.readlines())
data = json.loads(data_str)

conn = psycopg2.connect(CONN_STR)
conn.autocommit = True

cur = conn.cursor()
count = 0
for word in data:
    try:
        cur.execute("INSERT INTO words (word, skipped, correct, status, source) VALUES(%s, %s, %s, %s, %s) RETURNING wid",
                (word, 0, 0, 'approved' if args.verified == True else 'unverified', args.source))
        wordid = cur.fetchone()[0]
        prohibited_count = 0
        for prohibited in data[word]:
            prohibited_count = prohibited_count + 1
            cur.execute("INSERT INTO prohibited_words (wid, word, rank) VALUES(%s, %s, %s)",
                    (wordid, prohibited, prohibited_count))
        count = count + 1
    except Exception as e:
        print e

cur.close()
conn.close()

print 'Inserted ' + str(count) + ' words'
