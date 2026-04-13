import requests
import json
import time
import os

# get hero list
heroes_res = requests.get("https://api.opendota.com/api/heroes")
heroes_data = heroes_res.json()

id_to_name = {
    hero["id"]: hero["localized_name"].lower().replace(" ", "-")
    for hero in heroes_data
}

result = {}

for hero in heroes_data:
    hero_id = hero["id"]
    hero_name = id_to_name[hero_id]

    print(f"Processing {hero_name}...")

    res = requests.get(f"https://api.opendota.com/api/heroes/{hero_id}/matchups")
    matchups = res.json()

    # compute winrate
    processed = []
    for m in matchups:

        if m["games_played"] < 20:
            continue

        winrate = m["wins"] / m["games_played"]

        processed.append({
            "hero": id_to_name.get(m["hero_id"], "unknown"),
            "winrate": winrate
        })

    # sort by best counters
    processed.sort(key=lambda x: x["winrate"], reverse=True)

    # assign ranks
    for i, item in enumerate(processed):
        item["rank"] = i + 1

    result[hero_name] = processed

    time.sleep(1.2)

with open("data.json", "w") as f:
    json.dump(result, f, indent=2)