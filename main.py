import psycopg2
import api
import config
import sys

try:
    conn = psycopg2.connect(host=config.host, user=config.username, password=config.password, port=config.port, database='fut')
except:
    print "connection failed.\nExiting..."
    sys.exit()

cur = conn.cursor()
cards = api.get_all_cards(pages=611)
i = 0

for index, row in cards.iterrows():
    api.post_player(row, cur)
    i = i + 1
    sys.stdout.write("Number of Cards: %d   \r" % (i) )
    sys.stdout.flush()
print "\ndone"

conn.commit()
cur.close()
conn.close()
