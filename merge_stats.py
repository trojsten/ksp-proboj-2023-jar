import json
import sys
import os
from collections import defaultdict
from copy import deepcopy

import matplotlib.pyplot as plt


def merge(stats, tmp_stats):
    for key in tmp_stats:
        if isinstance(tmp_stats[key], dict):
            for key2 in tmp_stats[key]:
                stats[key][key2] += tmp_stats[key][key2]
        elif isinstance(tmp_stats[key], int):
            stats[key] += tmp_stats[key]


path = sys.argv[1]

ignore = -1

players = ["Armata", "CierneZeny", "Elerpe", "My", "RuzovyTank", "TankiOffline", "atsooi", "budapest", "dvaja_strateny",
           "gersiagi", "janci", "kockumamdoma", "kocurika", "kokorokjo", "krtko", "misqo", "okno",
           "pecenezemiaky", "poharvdzbane", "robotrt", "severnakambodza", "zrovnamebudapest", "stefan.exe", "tanky.io",
           "tiger"]

scores = defaultdict(lambda: 0)
scores_progress = defaultdict(lambda: [])
scores_progress_d = defaultdict(lambda: [])
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#000000', '#f7db8d', '#f78de7', '#4a013f', '#a0ff8f', '#71b9f0',
          '#f07171', '#ff8945', '#bdbdbd', '#ff0000', '#f6ff00', '#2e1100', '#00002e', '#578f77', '#1f4233']

stats = {
    "time_by_tank": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0},
    "score_by_reason": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
    "time_in_cooldown": 0, "time_not_in_cooldown": 0, "time_of_responses": 0,
    "stats": {
        "range": 0,
        "speed": 0,
        "bullet_speed": 0,
        "bullet_ttl": 0,
        "bullet_damage": 0,
        "health_max": 0,
        "health_regeneration": 0,
        "body_damage": 0,
        "reload_speed": 0
    }
}

player_stats = {}
for player in players:
    player_stats[player] = deepcopy(stats)

for (dirpath, dirnames, filenames) in os.walk(path):
    for dirname in dirnames:
        if dirname.startswith('game-'):
            if int(dirname[len('game-'):]) > ignore:
                try:
                    tmp_stats = json.load(open(path + os.sep + dirname + os.sep + "stats.json", 'r', encoding='utf-8'))
                    for player in tmp_stats:
                        merge(player_stats[player], tmp_stats[player])
                except Exception as e:
                    print(f"exception {e} in directory {dirname}")


json.dump(player_stats, open("statistics.json", "w"), indent=2)
