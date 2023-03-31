import json
import sys
import os
from collections import defaultdict, Counter
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

scores = {"Armata": 0, "CierneZeny": 0, "Elerpe": 0, "My": 0, "RuzovyTank": 0, "TankiOffline": 0, "atsooi": 0,
          "budapest": 0, "dvaja_strateny": 0, "gersiagi": 0, "janci": 0, "kockumamdoma": 0, "kocurika": 0,
          "kokorokjo": 0, "krtko": 0, "misqo": 0, "okno": 0, "pecenezemiaky": 0, "poharvdzbane": 0, "robotrt": 0,
          "severnakambodza": 0, "zrovnamebudapest": 0, "stefan.exe": 0, "tanky.io": 0, "tiger": 0}

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#000000', '#f7db8d', '#f78de7', '#4a013f', '#a0ff8f', '#71b9f0',
          '#f07171', '#ff8945', '#bdbdbd', '#ff0000', '#f6ff00', '#2e1100', '#00002e', '#578f77', '#1f4233']

tanks = {12: "AsymetricTripleTank", 4: "DoubleDoubleTank", 2: "EverywhereTank", 7: "GuidedBulletTank",
         11: "InvisibleBulletTank", 8: "MachineGunTank", 10: "PeacefulTank", 3: "VariableDoubleTank",
         6: "WideBulletTank", 1: "TwinTank", 5: "SniperTank", 9: "AsymetricTank", 0: "BasicTank"}

stats = json.load(open(sys.argv[1], "r"))

players = list(stats.keys())

# Time by tank
time_by_tank = {}
for i in [0, 1, 5, 9, 2, 3, 4, 6, 7, 8, 10, 11, 12]:
    time_by_tank[tanks[i]] = [stats[player]["time_by_tank"][str(i)] for player in players]

# print(time_by_tank)

left = np.zeros(len(players))

fig, ax = plt.subplots()

for boolean, weight_count in time_by_tank.items():
    p = ax.barh(players, weight_count, 0.75, label=boolean, left=left)
    left += weight_count

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.05,
                 box.width, box.height * 1.0])

ax.set_title("Time by tank")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=7, )

# plt.show()

# pie chart
cols = 4
fig, ax = plt.subplots(nrows=3, ncols=cols)
skipped = 0
for i, player in enumerate(players):
    sizes = [stats[player]["time_in_cooldown"], stats[player]["time_not_in_cooldown"]]
    labels = ["In cooldown", "Not in cooldown"]
    to_remove = []
    for j in range(len(sizes)):
        if sizes[j] == 0:
            to_remove.append(j)
    for j in reversed(to_remove):
        sizes.pop(j)
        labels.pop(j)
    if len(sizes) <= 1:
        skipped += 1
        continue
    ax[(i - skipped) // cols][(i - skipped) % cols].set_title(player)
    ax[(i - skipped) // cols][(i - skipped) % cols].pie(sizes, labels=labels, autopct='%1.2f%%', startangle=45)

fig.suptitle("Time in reload")
fig.tight_layout()

# plt.show()

categories = ["range", "speed", "bullet_speed", "bullet_ttl", "bullet_damage", "health_max", "health_regeneration",
              "body_damage", "reload_speed"]
categories = [*categories, categories[0]]

label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
for i, player in enumerate(players):
    vals = list(stats[player]["stats"].values())
    vals = vals + [vals[0]]
    vals = np.sqrt(vals)
    plt.plot(label_loc, vals, label=player)
plt.title('√(stat)', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend(loc="center left", bbox_to_anchor=(-0.5, 0.5), ncol=1, )
# plt.show()

plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
current_players = sorted(players, key=lambda x: scores[x])[:5]
for i, player in enumerate(current_players):
    vals = list(stats[player]["stats"].values())
    vals = vals + [vals[0]]
    vals = np.sqrt(vals)
    plt.plot(label_loc, vals, label=player)
plt.title('√(stat) posledných 5', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend(loc="center left", bbox_to_anchor=(-0.5, 0.5), ncol=1, )
# plt.show()


plt.figure(figsize=(8, 8))
plt.subplot(polar=True)
current_players = sorted(players, key=lambda x: scores[x])[-5:]
for i, player in enumerate(current_players):
    vals = list(stats[player]["stats"].values())
    vals = vals + [vals[0]]
    vals = np.sqrt(vals)
    plt.plot(label_loc, vals, label=player)
plt.title('√(stat) prvých 5', size=20)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
plt.legend(loc="center left", bbox_to_anchor=(-0.5, 0.5), ncol=1, )
# plt.show()

# score by reason
score_by_reason = {"0": "BodyDamagePlayer", "1": "BulletDamagePlayer", "2": "BodyDamageEntity",
                   "3": "BulletDamageEntity", "4": "KillPlayer", "5": "KillEntity"}
cols = 5
fig, ax = plt.subplots(nrows=5, ncols=cols)
patches = []
for i, player in enumerate(players):
    sizes = []
    labels = []
    for label, val in stats[player]["score_by_reason"].items():
        sizes.append(val)
        labels.append(score_by_reason[label])
    to_remove = []
    for j in range(len(sizes)):
        if sizes[j] == 0:
            to_remove.append(j)
    for j in reversed(to_remove):
        sizes.pop(j)
        labels.pop(j)
    if len(sizes) <= 1:
        skipped += 1
        continue
    ax[(i - skipped) // cols][(i - skipped) % cols].set_title(player)
    patches, texts, autotexts = ax[(i - skipped) // cols][(i - skipped) % cols].pie(sizes,
                                                                                    autopct=lambda pct: ('%1.2f%%' % pct) if pct > 0 else '',
                                                                                    startangle=45,
                                                                                    pctdistance=1.25,)
fig.legend(patches, labels, ncol=6, loc="lower center")
fig.suptitle("Score by reason")
plt.tight_layout(pad=0, w_pad=0, h_pad=0)
fig.subplots_adjust(bottom=0.05)

# time_of_responses
fig, ax = plt.subplots()
sizes = []
labels = []
for player in players:
    sizes.append(stats[player]["time_of_responses"])
    labels.append(player)
ax.set_title("Time of responses")
ax.pie(sizes, labels=labels,
       autopct=lambda pct: ('%1.2f%%' % pct) if pct > 0 else '',
       startangle=45,
       pctdistance=1.15,
       labeldistance=1.27)
# fig.legend(patches, labels, ncol=6, loc="lower center")

plt.show()

