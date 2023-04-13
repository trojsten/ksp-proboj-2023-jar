#!/bin/env python3
import random
from math import inf
import dodge
from shoot import *
from evolve import *

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(
            velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
            shoot=OneBulletShoot(6.28 * random.random()),
            stat=StatsEnum.StatNone,
            new_tank_id=0,
        )


class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        nearest = XY(inf, inf)

        is_player = False

        for entity in self.entities:
            if self.myself.position.distance(
                entity.position
            ) < self.myself.position.distance(nearest):
                nearest = entity.position

        for player in self.players.values():
            if player != self.myself:
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

        if (
            self.myself.position.distance(move)
            < self.myself.stat_values[StatsEnum.StatBulletTTL]
            * self.myself.stat_values[StatsEnum.StatBulletSpeed]
        ):
            move = self.myself.position

        if (
            self.myself.position.x < self.world.min_x
            or self.myself.position.x > self.world.max_x
            or self.myself.position.y < self.world.min_y
            or self.myself.position.y > self.world.max_y
        ):
            move = XY(0, 0)

       
        my_target = find_target(self)

        my_strategy=Strategy.get_strategy(3)
        my_upgrade = chose_evolution(self, my_strategy.endpoint)
        my_stat = StatsEnum.StatNone
        if self.myself.levels_left>0:
            my_stat=chose_stat(self, my_strategy)
        return Turn(
            velocity=dodge.dodge_strategy(self, move - self.myself.position),
            shoot=my_target,
            stat=my_stat,
            new_tank_id=my_upgrade,
        )


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
