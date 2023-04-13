#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

from stefanlib import move
# from stefanlib.move import get_move_target, get_move_vector
from stefanlib.utils import nearest_entity, nearest_player
from stefanlib.shot import get_shot
from stefanlib.upgrades import suggest_upgrade, suggest_tank


class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        self.log(f"mame {self.myself.lifes_left} zivotov")
        shot = get_shot(self)
        return Turn(velocity=move.get_move_vector(move.get_move_target(self), self),
                    shoot=shot,
                    stat=suggest_upgrade(self),
                    new_tank_id=suggest_tank(self))

    def dummy_upgrade(self):
        if self.myself.levels_left == 0:
            return StatsEnum.StatNone

        return StatsEnum.StatSpeed\
            if self.myself.stat_levels[StatsEnum.StatSpeed] <= self.myself.stat_levels[StatsEnum.StatRange]\
            else StatsEnum.StatRange

    #aaaaaaaaaaaaaaa


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
