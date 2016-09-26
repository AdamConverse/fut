import psycopg2
import api
import fut
import config
import sys
import time
import random


def update_player_database(cur, pages=0):
    """Update player FUT database. Skips card if found by id."""
    cards = api.get_all_cards(pages)
    i = 0
    for index, row in cards.iterrows():
        api.post_player(row, cur)
        i = i + 1
        sys.stdout.write("Number of Cards: %d   \r" % (i))
        sys.stdout.flush()
    print "\ndone"
    return


def stream_market_scrape(cur):
    """Stream output of current progress of market scrape."""
    fut_conn = fut.Core(config.email, config.password, config.secret_answer, code=config.code, platform=config.platform, debug=False)
    i = 0
    page = 1
    stop = False
    while stop is False:
        items = fut_conn.searchAuctions('player', start=page, level='gold')
        if len(items) < 1:
            continue
        for item in items:
            api.post_transaction(item, cur)
            i = i + 1
        page += 1
        print "Expires:" + str(items[0]["expires"])
        print "Page:" + str(page)
        print "Number of cards: " + str(i) + "\n"
        time.sleep(random.randint(1,3))
    print "\ndone"
    return


if __name__ == "__main__":
    try:
        conn = psycopg2.connect(host=config.host, user=config.username, password=config.password, port=config.port, database='fut')
    except:
        print "connection failed.\nExiting..."
        sys.exit()
    cur = conn.cursor()

    stream_market_scrape(cur)

    conn.commit()
    cur.close()
    conn.close()
