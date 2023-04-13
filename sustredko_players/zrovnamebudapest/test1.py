#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        nearest = XY(200 * random.random() - 100, 200 * random.random() - 100)

        self.log('spisovatel   ', self.myself.position.angle_to(nearest))

        return Turn(velocity=nearest,
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class LepsiPlayer(ProbojPlayer):

    
    def make_turn(self) -> Turn:
        zbijem_ta = XY(0, 0)
        nearest = XY(inf, inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                zbijem_ta = entity.position

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                    zbijem_ta = player.position

        ttl = 'nemas naboj brasko'

        skalarny_dostrel = ":'("
        for bullet in self.bullets:
            
            ttl = bullet.ttl
            skalarny_dostrel = ttl * self.myself.position.distance(bullet.position)
            self.log('hups ...', bullet.shooter_id)







        nearest = XY(0, 0)

        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0

        return Turn(velocity=nearest - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(zbijem_ta)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
