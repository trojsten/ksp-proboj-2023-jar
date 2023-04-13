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

    
    def make_turn(self) -> Turn:
        nearest = XY(inf, inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                nearest = entity.position

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                    nearest = player.position

        ttl = 'nemas naboj brasko'
        pos_naboj = 'fakt ho nemas'
        rychlost_naboj = 'nic nebude'
        skalarny_dostrel = ''
        for bullet in self.bullets:
            
            ttl = bullet.ttl
            pos_naboj = bullet.position
            rychlost_naboj = bullet.velocity
            skalarny_dostrel = ttl * self.myself.position.distance(bullet.position)

            





        self.log("tvoja mama na pozicii ", self.myself.position)
        self.log("tak a teraz ta zastrelim ", 'dostrel este >', skalarny_dostrel)
        self.log("ideme na", nearest.x, nearest.y)

        if nearest == XY(inf, inf):
            nearest = XY(0, 0)

        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0

        return Turn(velocity=nearest - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
