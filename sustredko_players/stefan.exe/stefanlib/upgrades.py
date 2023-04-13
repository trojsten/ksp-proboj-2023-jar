import collections
import copy
import random

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

h = {
    0: StatsEnum.StatRange,
    1: StatsEnum.StatHealthRegeneration,
    2: StatsEnum.StatHealthMax,
    3: StatsEnum.StatBodyDamage,
    4: StatsEnum.StatBulletSpeed,
    5: StatsEnum.StatBulletTTL,
    6: StatsEnum.StatBulletDamage,
    7: StatsEnum.StatReloadSpeed,
    8: StatsEnum.StatSpeed
}

#guided
q_guided1_1 = [
    5,6,0,4,7, 5,7,5,4,5,
    6,6,7,5,5,6, 4,5,6,7,
    1,2,8,6,6, 7,7,1,2,8]
q_guided1_1 = [
    5,6,0,0,6, 0,0,6,5,4,
    6,6,7,7,5,5, 6,6,7,5,
    5,7,5,7,5, 2,1,8,8,4]
# q_guided1_2 = copy.deepcopy(q_guided1_1)
q_guided1_3 = [
    6,5,0,6,5, 6,6,4,7,5,
    6,5,0,7,5,6, 6,5,7,4,
    4,5,5,7,7, 7,7,2,2,2
    ]

# q_bodydamage1 = collections.deque([
#     3,2,1,2,2, 3,8,3,8,1,
#     0,1,8,2,0,3, 2,8,2,1,
#     1,1,8,3,3, 2,1,3,8,8])
#
# q_bodydamage2 = collections.deque([
#     0,0,3,8,2, 1,2,2,3,0,
#     8,3,8,3,8,2, 1,2,2,3,
#     2,1,1,3,8, 1,8,1,8,3])


q1 = q_guided1_1[:]
q2, q3, q4 = q1[:], q1[:], q1[:]
def suggest_upgrade(self: ProbojPlayer) -> StatsEnum:
    me = self.myself
    upgrade = StatsEnum.StatReloadSpeed

    if me.levels_left:

        if me.lifes_left == 3:
            if not q3:
                return StatsEnum.StatRange
            upgrade = h[q3.pop(0)]
        elif me.lifes_left == 2:
            if not q2:
                return StatsEnum.StatRange
            upgrade = h[q2.pop(0)]
        elif me.lifes_left == 1:
            if not q1:
                return StatsEnum.StatRange
            upgrade = h[q1.pop(0)]
        elif me.lifes_left == 0:
            if not q4:
                return StatsEnum.StatRange
            upgrade = h[q4.pop(0)]

    else:
        upgrade = StatsEnum.StatNone

    self.log(f"Upgrading {upgrade.name}")
    return upgrade

#3rd life alternation
def suggest_body_upgrade(self:ProbojPlayer) -> int:
    me = self.myself
    tank = 0
    if me.tank_updates_left > 0:
        if me.tank.tank_id == 0:
            tank = 9
        if me.tank.tank_id == 9:
            tank = 10

    self.log(f"Tank upgrade: {tank}")
    return tank

#2nd life alt


#1st & 2nd life
def suggest_tank(self: ProbojPlayer) -> int:
    me = self.myself

    #3rd life
    # if me.lifes_left == 1:
    #     return suggest_body_upgrade(self)

    tank = 0
    if me.tank_updates_left > 0:
        # Guided
        if me.tank.tank_id == 0:
            tank = 5
        if me.tank.tank_id == 5:
            tank = 7

        # # Invis
        # if me.tank.tank_id == 0:
        #     tank = 9
        # if me.tank.tank_id == 9:
        #     tank = 11

    self.log(f"Tank upgrade: {tank}")
    return tank
