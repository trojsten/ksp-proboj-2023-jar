#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
x = 0
z = 0
a = 0
class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        global x,z,a
        nearest = XY(inf, inf)
        nearest_player_pos = XY(inf, inf)
        q, p = 0, 0
        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                if self.world.max_x > entity.position.x > self.world.min_x and self.world.max_y > entity.position.y > self.world.min_y:
                    nearest = entity.position
                    q = 1

        if self.myself.level >= 20:
            for player in self.players.values():
                if player != self.myself:
                    if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_player_pos):
                        nearest_player_pos = player.position
                        nearest_player_id = player.id
                        p = 1


        
        stred_x = (self.world.max_x + self.world.min_x)/2
        stred_y = (self.world.max_y + self.world.min_y)/2
        
        if q != 1:
            nearest = XY(stred_x+200,stred_y+200)
        if self.myself.position == nearest:
            nearest = XY(stred_x+200,stred_y-200)  
        elif self.myself.position == nearest:
            nearest = XY(stred_x-200,stred_y-200)  
        elif self.myself.position == nearest:
            nearest = XY(stred_x-200,stred_y+200)  

        if len(self.myself.tank.updatable_to)!=0:
            if self.myself.level <= 10:
                update_to = 5
            else:
                update_to = 7
        else:
            update_to = 0
        
        nearestoriginal = nearest #vylepsit
        if x % 7 == 0:
                vyber = StatsEnum.StatSpeed
        elif x % 7 == 1:
                vyber = StatsEnum.StatBulletTTL
        elif x % 7 == 2:
                vyber = StatsEnum.StatBulletDamage
        elif x % 7 == 5 or x % 7 == 3:
             vyber = StatsEnum.StatReloadSpeed
        elif x % 7 == 6:
            vyber = StatsEnum.StatHealthMax
        elif x % 7 == 4:
            vyber = StatsEnum.StatRange
        x += 1

        if self.myself.position.distance(nearest) < 100:
            nearest = self.myself.position

        if self.bullets == True:
            if a // 10 != 0:
                a1 = random.randint(self.world.min_x,self.world.max_x)
                a2 = random.randint(self.world.min_y,self.world.max_y)
                a = a // 10
            else:
                a += 1
            nearest = XY(a1, a2)
        else:
            a = 0
        if self.myself.level <20:   
            return Turn(velocity=nearest - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearestoriginal)),
                    stat = vyber,
                    new_tank_id=update_to)
        else:
            if p == 1:
               return Turn(velocity=nearest_player_pos - self.myself.position,
                       shoot=PlayerShoot(nearest_player_id),
                       stat=vyber,
                       new_tank_id=update_to)
            if p == 0:
                return Turn(velocity=nearest - self.myself.position,
                        shoot=XyShoot(nearestoriginal),
                        stat=vyber,
                        new_tank_id=update_to)
            
if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
