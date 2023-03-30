import json
import sys
import os
from collections import defaultdict
import matplotlib.pyplot as plt

path = sys.argv[1]
out = sys.argv[2]

ignore = 300

players = {"Armata", "CierneZeny", "Elerpe", "My", "RuzovyTank", "TankiOffline", "atsooi", "budapest", "dvaja_strateny",
           "gersiagi", "janci", "kockumamdoma", "kocurika", "kokorokjo", "krtko", "misqo", "najlepsi", "okno",
           "pecenezemiaky", "poharvdzbane", "robotrt", "severnakambodza", "stefan.exe", "tanky.io", "tiger"}

scores = defaultdict(lambda: 0)
scores_progress = defaultdict(lambda: [])
scores_progress_d = defaultdict(lambda: [])
d = 50
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#000000', '#f7db8d', '#f78de7', '#4a013f', '#a0ff8f', '#71b9f0',
          '#f07171', '#ff8945', '#bdbdbd', '#ff0000', '#f6ff00', '#2e1100', '#00002e', '#578f77', '#1f4233']
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
                            scores[player] += 0
                except:
                    pass

for player in sorted(players):
    for i in range(len(scores_progress[player]) - d):
        scores_progress_d[player].append(scores_progress[player][i+d]-scores_progress[player][i])

json.dump(scores, open(out + '-scores.json', 'w'))
json.dump(scores_progress, open(out + '-scores-progress.json', 'w'), indent=2)

plt.figure(dpi=200, figsize=(15, 10))
for i, p in enumerate(sorted(players)):
    plt.plot(scores_progress[p], label=p, color=colors[i % len(colors)])
plt.legend()
# plt.show()
plt.title("Body")
plt.savefig(out + '-scores.png')

plt.figure(dpi=200, figsize=(15, 10))
for i, p in enumerate(sorted(players)):
    plt.plot(scores_progress_d[p], label=p, color=colors[i % len(colors)])
plt.legend()
# plt.show()
plt.title("Prvá derivácia počtu bodov")
plt.savefig(out + '-scores-d.png')
