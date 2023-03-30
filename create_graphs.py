import json
import sys
import os
from collections import defaultdict
import matplotlib.pyplot as plt

path = sys.argv[1]
out = sys.argv[2]

ignore = 300

players = {"Armata", "CierneZeny", "Elerpe", "My", "RuzovyTank", "TankiOffline", "atsooi", "budapest", "dvaja_strateny",
           "FeRR1te", "janci", "kockumamdoma", "kocurika", "kokorokjo", "krtko", "misqo", "najlepsi", "okno",
           "Pečené zemiaky",
           "poharvdzbane", "roboTRT", "Severná kambodža", "stefan.exe", "tanky.io", "tiger"}

scores = defaultdict(lambda: 0)
scores_progress = defaultdict(lambda: [])
scores_progress_d = defaultdict(lambda: [])
d = 2

score_len = 0

for (dirpath, dirnames, filenames) in os.walk(path):
    for dirname in dirnames:
        if dirname.startswith('game-'):
            if int(dirname[len('game-'):]) > ignore:
                try:
                    tmp_scores = json.load(open(path + os.sep + dirname + os.sep + "score", 'r', encoding='utf-8'))
                    updated = set()
                    for player in tmp_scores:
                        scores_progress[player].append(tmp_scores[player] + scores[player])
                        scores[player] += tmp_scores[player]
                        score_len = max(score_len, len(scores))
                        updated.add(player)
                    for player in players:
                        if player not in updated:
                            scores_progress[player].append(scores[player])
                except:
                    pass

for i in range(score_len - d):
    for player in players:
        scores_progress_d[player].append(sum(scores_progress[player][i:i + d]))

json.dump(scores, open(out + '-scores.json', 'w'))
json.dump(scores_progress, open(out + '-scores-progress.json', 'w'), indent=2)

plt.figure(dpi=500, figsize=(15, 10))
for p in scores_progress:
    plt.plot(scores_progress[p], label=p)
plt.legend()
# plt.show()
plt.savefig(out + '-scores.png')

plt.figure(dpi=500, figsize=(15, 10))
for p in scores_progress_d:
    plt.plot(scores_progress_d[p], label=p)
plt.legend()
# plt.show()
plt.savefig(out + '-scores-d.png')
