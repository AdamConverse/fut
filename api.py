import config
import fut
import json
import urllib
import json
import pandas as pd


def get_all_cards(pages=1):
    """Get all cards from EA."""
    good_columns = ["id", "baseId", "name", "position", "quality", "color", "rating"]
    temp = []
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
    cur.execute("""INSERT INTO fut_players (id, name, club_id, position, quality, card_type, base_id, rating, nation) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""", [int(data["id"]), data["name"], int(data["club_id"]), data["position"], data["quality"], data["color"], int(data["baseId"]), int(data["rating"]), data["nation"]])
    return


def temp():
    """."""
    fut = fut.Core(config.email, config.password, config.secret_answer, code=config.code, platform=config.platform, debug=True)
