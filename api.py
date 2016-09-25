import config
import json
import urllib
import json
import pandas as pd


def get_all_cards(pages=0):
    """Get all cards from EA."""
    good_columns = ["id", "baseId", "name", "position", "quality", "color", "rating"]
    temp = []
    url = "https://www.easports.com/fifa/ultimate-team/api/fut/item?page=1"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    total_pages = data["totalPages"]
    if pages is 0:
        pages = total_pages
    for page in range(pages):
        url = "https://www.easports.com/fifa/ultimate-team/api/fut/item?page=" + str(page)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for item in data["items"]:
            player = {}
            for key in good_columns:
                player[key] = item[key]
            player["club_id"] = item["club"]["id"]
            player["nation"] = item["nation"]["name"]
            temp.append(player)
    return pd.DataFrame(temp)


def post_player(data, cur):
    """Post player to database."""
    cur.execute("""INSERT INTO fut_players (id, name, club_id, position, quality, card_type, base_id, rating, nation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING""",
        [int(data["id"]), data["name"], int(data["club_id"]), data["position"], data["quality"], data["color"], int(data["baseId"]), int(data["rating"]), data["nation"]])
    return


def post_transaction(data, cur):
    """Post transaction to database."""
    cur.execute("""INSERT INTO fut_transactions (sellerEstablished, rating, itemType, resourceId, expires, cardType, formation,
        leagueId, watched, tradeState, id, sellerId, owners, tradeId, assetId, sellerName, buyNowPrice, injuryType, lastSalePrice, offers, startingBid,
        timestamp, itemState, currentBid, bidState, rareflag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING""",
        [data["sellerEstablished"], data["rating"], data["itemType"], data["resourceId"], data["expires"], data["cardType"], data["formation"], data["leagueId"], data["watched"],
        data["tradeState"], data["id"], data["sellerId"], data["owners"], data["tradeId"], data["assetId"], data["sellerName"], data["buyNowPrice"], data["injuryType"], data["lastSalePrice"],
        data["offers"], data["startingBid"], data["timestamp"], data["itemState"], data["currentBid"], data["bidState"], data["rareflag"]])
    return


def get_player(player_id, cur):
    """Get player from database by id."""
    cur.execute("""SELECT * FROM fut_players WHERE id = %s;""", [player_id])
    return cur.fetchone()
