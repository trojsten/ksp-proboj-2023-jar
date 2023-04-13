#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *



class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        neareste = XY(inf, inf)
        nearestp = XY(inf, inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(neareste):
                neareste = entity.position

        for player in self.players.values():
            if player != self.myself:
                # self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearestp):
                    nearestp = player.position

        # self.log("ideme na", nearest.x, nearest.y)

        if nearestp != XY(inf, inf) and self.myself.position.distance(nearestp)<2500:
            nearest = nearestp
        else:
            nearest= neareste
            if nearest == XY(inf, inf):
                nearest = self.myself.position
                
        if self.myself.position.distance(nearest) < 150:
            vel = XY(random.randint(-100,100),random.randint(-100,100))
        else:
            vel = nearest - self.myself.position
        
        vx,vy=0,0
        if abs(self.world.min_x-self.myself.position.x) < 250:
            vx=1000
        if abs(self.world.max_x-self.myself.position.x) < 250:
            vx=-1000
        if abs(self.world.min_y-self.myself.position.y) < 250:
            vy=1000
        if abs(self.world.max_y-self.myself.position.y) < 250:
            vy=-1000
        if vx!=0 or vy!=0:
            vel = XY(vx,vy)
            
        
        
        
        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice([1,5,6])
        else:
            update_to = 0
        
            
        new_stat = random.choice([StatsEnum.StatRange ,
        StatsEnum.StatSpeed ,
        StatsEnum.StatBulletSpeed ,
        StatsEnum.StatBulletTTL ,
        StatsEnum.StatBulletDamage ,
        StatsEnum.StatHealthMax ,
        StatsEnum.StatHealthRegeneration ,
        StatsEnum.StatBodyDamage ,
        StatsEnum.StatReloadSpeed])
        return Turn(velocity=vel,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                    stat=new_stat,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
