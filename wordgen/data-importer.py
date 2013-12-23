#!/usr/bin/env python
import sys, json, psycopg2

CONN_STR = 'dbname=prod user=prod'

data_str = '\n'.join(sys.stdin.readlines())
data = json.loads(data_str)

conn = psycopg2.connect(CONN_STR)

cur = conn.cursor()
count = 0
for word in data:
    cur.execute("INSERT INTO words (word, skipped, correct) VALUES(%s, %s, %s) RETURNING id",
            (word, 0, 0))
    wordid = cur.fetchone()[0]
    for prohibited in data[word]:
        cur.execute("INSERT INTO prohibited_words (wordid, word) VALUES(%s, %s)",
                (wordid, prohibited))
    count = count + 1

conn.commit()
cur.close()
conn.close()

print 'Inserted ' + str(count) + ' words'
