import psycopg2
import api
import fut
import config
import sys
import time


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


def stream_market_scrape(cur, pages=0):
    """Stream output of current progress of market scrape."""
    fut_conn = fut.Core(config.email, config.password, config.secret_answer, code=config.code, platform=config.platform, debug=True)
    i = 0
    if pages is 0:
        pages = 100
    for page in range(pages):
        items = fut_conn.searchAuctions('player', start=100+page, level='gold')
        for item in items:
            api.post_transaction(item, cur)
            i = i + 1
            sys.stdout.write("Number of Cards: %d   \r" % (i))
            sys.stdout.flush()
        time.sleep(.1)
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