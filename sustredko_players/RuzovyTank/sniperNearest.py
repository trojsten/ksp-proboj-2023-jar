#!/bin/env python3
import random
from math import inf
import dodge
from movement import adjust_move
from shoot import *
from evolve import *

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
from parameters import parameters


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(
            velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
            shoot=OneBulletShoot(6.28 * random.random()),
            stat=StatsEnum.StatNone,
            new_tank_id=0,
        )


class LepsiPlayer(ProbojPlayer):
    def __init__(self):
        self.parameters = parameters

    def make_turn(self) -> Turn:
        self.gun_range = (
            self.myself.stat_values[StatsEnum.StatBulletTTL]
            * self.myself.stat_values[StatsEnum.StatBulletSpeed]
        )
        nearest = XY(inf, inf)

        is_player = False

        for entity in self.entities:
            if self.myself.position.distance(
                entity.position
            ) < self.myself.position.distance(nearest):
                nearest = entity.position

        for player in self.players.values():
            if player.id != self.myself.id:
                self.log(
                    "vidim hraca", player.id, "na", player.position.x, player.position.y
                )
                if not is_player or self.myself.position.distance(
                    player.position
                ) < self.myself.position.distance(nearest):
                    nearest = player.position
                    is_player = True

        self.log("ideme na", nearest.x, nearest.y)

        if nearest == XY(inf, inf):
            nearest = XY(0, 0)

        move = nearest

        my_target = shoot_nearest(self)
        my_strategy = Strategy.get_strategy(2)
        my_upgrade = chose_evolution(self, my_strategy.endpoint)
        my_stat = StatsEnum.StatNone
        if self.myself.levels_left > 0:
            my_stat = chose_stat(self, my_strategy)
        return Turn(
            velocity=adjust_move(self, move - self.myself.position),
            shoot=my_target,
            stat=my_stat,
            new_tank_id=my_upgrade,
        )


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
