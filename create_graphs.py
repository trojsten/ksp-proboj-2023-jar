import json
import sys
import os
from collections import defaultdict
import matplotlib.pyplot as plt

path = sys.argv[1]
out = sys.argv[2]

ignore = 2

scores = defaultdict(lambda: 0)
scores_progress = defaultdict(lambda: [])
scores_progress_d = defaultdict(lambda: [])
d = 2

score_len = 0

for (dirpath, dirnames, filenames) in os.walk(path):
    for dirname in dirnames:
        if dirname.startswith('game-'):
            if int(dirname[len('game-'):]) > ignore:
                tmp_scores = json.load(open(path + os.sep + dirname + os.sep + "score", 'r', encoding='utf-8'))
                for player in tmp_scores:
                    scores_progress[player].append(tmp_scores[player] + scores[player])
                    if len(scores_progress) > d:
                        scores_progress_d[player].append(scores_progress[player][-1]-scores_progress[player][-d+1])
                    scores[player] += tmp_scores[player]
                    score_len = max(score_len, len(scores))

json.dump(scores, open(out + '-scores.json', 'w'))
json.dump(scores_progress, open(out + '-scores-progress.json', 'w'))

plt.figure()
for p in scores_progress:
    plt.plot(scores_progress[p])
# plt.show()
plt.savefig(out + '-scores.png')


plt.figure()
for p in scores_progress_d:
    plt.plot(scores_progress_d[p])
# plt.show()
plt.savefig(out + '-scores-d.png')
