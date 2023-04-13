#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class LepsiPlayer(ProbojPlayer):

    def __init__(self):
        self.level = -1
        self.strielam = True

    def make_turn(self) -> Turn:
        nearest = XY(inf, inf)

        if TwinTank in self.myself.tank.updatable_to:
            update_to = 1
        else: update_to = 4


        upStats = [StatsEnum.StatRange, StatsEnum.StatBulletTTL, StatsEnum.StatBulletTTL, StatsEnum.StatBulletTTL,  StatsEnum.StatBulletTTL, StatsEnum.StatReloadSpeed, StatsEnum.StatReloadSpeed, StatsEnum.StatReloadSpeed, StatsEnum.StatBulletDamage, StatsEnum.StatReloadSpeed, StatsEnum.StatHealthRegeneration, StatsEnum.StatBulletDamage, StatsEnum.StatReloadSpeed, StatsEnum.StatBulletDamage, StatsEnum.StatReloadSpeed, StatsEnum.StatRange, StatsEnum.StatBulletDamage, StatsEnum.StatReloadSpeed, StatsEnum.StatBulletDamage, StatsEnum.StatBulletDamage, StatsEnum.StatBulletDamage, StatsEnum.StatRange, StatsEnum.StatRange, StatsEnum.StatBulletTTL, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletTTL, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletTTL, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletTTL, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletSpeed, StatsEnum.StatSpeed, StatsEnum.StatSpeed, StatsEnum.StatSpeed, StatsEnum.StatSpeed] * 100

        self.log(len(upStats))
        
        upstat = StatsEnum.StatNone

        
        if self.myself.levels_left > 0:
            self.level += 1
            upstat = upStats[self.level]
        
        nearest_player = None

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                    nearest = player.position
                    nearest_player = player


        if nearest_player is not None:
            return Turn(velocity=self.myself.position-nearest if nearest_player.tank == 10 else nearest - self.myself.position,
                shoot=OneBulletShoot(self.myself.position.angle_to(nearest) if self.myself.stat_values.stats[StatsEnum.StatBulletTTL.value]*self.myself.stat_values.stats[StatsEnum.StatBulletSpeed.value] >= self.myself.position.distance(nearest) else -self.myself.position.angle_to(nearest)),
                stat=upstat,
                new_tank_id=update_to)
        

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                self.strielam = True
                nearest = entity.position


        
        if nearest == XY(inf, inf):
            nearest = XY(0, 0)
            self.strielam = False

        self.log("ideme na", nearest.x, nearest.y)

        return Turn(velocity=nearest - self.myself.position,
                shoot=NoShoot if not self.strielam else OneBulletShoot(self.myself.position.angle_to(nearest) if self.myself.stat_values.stats[StatsEnum.StatBulletTTL.value]*self.myself.stat_values.stats[StatsEnum.StatBulletSpeed.value] >= self.myself.position.distance(nearest) else -self.myself.position.angle_to(nearest)),
                stat=upstat,
                new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
