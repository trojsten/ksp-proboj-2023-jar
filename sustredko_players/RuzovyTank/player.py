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
        self.tgpos = None

    def make_turn(self) -> Turn:
        self.gun_range = (
            self.myself.stat_values[StatsEnum.StatBulletTTL]
            * self.myself.stat_values[StatsEnum.StatBulletSpeed]
        )
        nearest = XY(inf, inf)

        is_player = False

        for entity in self.entities:
            if entity.position.x < self.world.min_x:
                continue
            if entity.position.y < self.world.min_y:
                continue
            if entity.position.x > self.world.max_x:
                continue
            if entity.position.y > self.world.max_y:
                continue
            if self.myself.position.distance(
                entity.position
            ) < self.myself.position.distance(nearest):
                nearest = entity.position
                self.tgpos = None

        """
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
        """

        self.log("ideme na", nearest.x, nearest.y)

        if math.isinf(nearest.x):
            if (
                self.tgpos is None
                or self.tgpos.distance(self.myself.position)
                < self.myself.stat_values[StatsEnum.StatSpeed]
            ):
                self.tgpos = XY(
                    random.randint(self.world.min_x, self.world.max_x),
                    random.randint(self.world.min_y, self.world.max_y),
                )
            nearest = self.tgpos

        move = nearest

        if len(self.myself.tank.updatable_to) != 0:
            update_to = random.choice(
                [tank.tank_id for tank in self.myself.tank.updatable_to]
            )
        else:
            update_to = 0

        stat_update = StatsEnum.StatNone
        if self.myself.levels_left > 0:
            stat_update = random.choice(
                [
                    StatsEnum.StatBulletDamage,
                    StatsEnum.StatBulletSpeed,
                    StatsEnum.StatHealthMax,
                    StatsEnum.StatHealthRegeneration,
                    StatsEnum.StatRange,
                    StatsEnum.StatReloadSpeed,
                    StatsEnum.StatSpeed,
                ]
            )
        
        self.my_target = shoot_nearest(self)
        self.log(self.my_target)
        self.my_strategy = Strategy.get_strategy(4)
        self.my_upgrade = chose_evolution(self)
        self.my_stat = StatsEnum.StatNone
        if self.myself.levels_left > 0:
            self.my_stat = chose_stat(self)
        self.log(self.my_stat)
        return Turn(
            velocity=adjust_move(self, move - self.myself.position),
            shoot=self.my_target,
            stat=self.my_stat,
            new_tank_id=self.my_upgrade,
        )



if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
