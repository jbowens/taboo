#!/usr/bin/env python
import sys, json, psycopg2, argparse

parser = argparse.ArgumentParser(description='Imports word data into the taboo database.')
parser.add_argument('--verified', dest='verified', action='store_true', help='include if these words are verified as good quality')
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
        cur.execute("INSERT INTO words (word, skipped, correct, verified) VALUES(%s, %s, %s, %s) RETURNING id",
                (word, 0, 0, args.verified == True))
        wordid = cur.fetchone()[0]
        for prohibited in data[word]:
            cur.execute("INSERT INTO prohibited_words (wordid, word) VALUES(%s, %s)",
                    (wordid, prohibited))
        count = count + 1
    except Exception as e:
        print e

cur.close()
conn.close()

print 'Inserted ' + str(count) + ' words'
