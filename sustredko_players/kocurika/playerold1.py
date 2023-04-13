#!/bin/env python3\
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

# self.world.minx
class MojPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        go_pos = XY(inf, inf)
        shoot_pos = XY(inf,inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(shoot_pos):
                shoot_pos = entity.position

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(shoot_pos):
                    shoot_pos = player.position

        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0
        
        if (shoot_pos == XY(inf, inf)):
            log("nic nevidim")
            go_pos = XY(0,0)
        else:
            stayr = 50
            if (self.myself.position.x >= shoot_pos.x):
                go_pos.x = shoot_pos.x+stayr
            else:
                go_pos.x = shoot_pos.x-stayr
            
            if (self.myself.position.y >= shoot_pos.y):
                go_pos.y = shoot_pos.y+stayr
            else:
                go_pos.y = shoot_pos.y-stayr

        self.log("som na", self.myself.position.x, self.myself.position.y)
        self.log("ideme na", go_pos.x, go_pos.y)
        self.log("strielam na", shoot_pos.x, shoot_pos.y)

        if shoot_pos != XY(inf, inf):
            return Turn(velocity=go_pos - self.myself.position,
                        shoot=OneBulletShoot(self.myself.position.angle_to(shoot_pos)),
                        stat=StatsEnum.StatNone,
                        new_tank_id=update_to)
        else:
            return Turn(velocity=go_pos - self.myself.position,
                        shoot=NoShoot(),
                        stat=StatsEnum.StatNone,
                        new_tank_id=update_to)


if __name__ == "__main__":
    p = MojPlayer()
    p.run()
