#!/usr/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

maxzakladhealth = 100
lastlevel = 0
poradieupgr = [0,
               StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatBulletDamage,
               StatsEnum.StatBulletDamage,StatsEnum.StatBulletDamage,StatsEnum.StatSpeed,
               StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,
               StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,
               StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,
               StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,
               StatsEnum.StatBodyDamage,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,
               StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed]
lastlives = 3


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class LepsiPlayer(ProbojPlayer):
    
    def make_turn(self) -> Turn:

        global lastlevel,lastlives

        ciel = [0,0]
        
        if self.myself.position.distance(XY(self.world.min_x,0)) < self.myself.position.distance(XY(self.world.max_x,0)):
            ciel[0] = self.world.min_x + 200
        else:
            ciel[0] = self.world.max_x - 200
        
        if self.myself.position.distance(XY(0,self.world.min_y)) < self.myself.position.distance(XY(0,self.world.max_y)):
            ciel[1] = self.world.min_y + 200
        else:
            ciel[1] = self.world.max_y - 200
        


        nearest = XY(inf, inf)

        pohyb = XY(ciel[0],ciel[1]) - self.myself.position

        if self.myself.lifes_left < lastlives:
            self.log("""
            preco som skapaaaal

            """)
            lastlevel = 0


        for entity in self.entities:
            if self.world.min_x + 200 < entity.position.x < self.world.max_x - 200 and self.world.min_y + 200 < entity.position.y < self.world.max_y - 200:
                if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                    nearest = entity.position
        
        
        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                nearest = player.position
        

        if nearest.x == inf and nearest.y == inf:
            nearest = XY(ciel[0], ciel[1])
        



        self.log(self.myself.stat_levels)
        statynavylep=[StatsEnum.StatNone]
        if self.myself.level > lastlevel:
            statynavylep = [poradieupgr[lastlevel+1]]
            lastlevel += 1

        '''
        for level in self.myself.stat_levels:
            if i == 5:
                self.log("i=",i,"levels=",level)
                if level < 3:
                    statynavylep.append(StatsEnum.StatBulletDamage)
            
            if i == 2:
                self.log("i=",i,"levels=",level)
                if level < 10:
                    statynavylep.append(StatsEnum.StatSpeed)
                else:
                    statynavylep.append(StatsEnum.StatHealthRegeneration)
                    statynavylep.append(StatsEnum.StatHealthMax)
                    statynavylep.append(StatsEnum.StatBodyDamage)

        '''


        if self.myself.tank.tank_id != 10:


            if self.myself.position.distance(nearest) < 75:
                pohyb = self.myself.position


            elif self.myself.position.distance(nearest) < 100:
                if self.myself.reload_cooldown == 0:
                    pohyb = nearest - self.myself.position
                else:
                    pohyb = self.myself.position

            else:
                pohyb = nearest - self.myself.position
            
            
            self.log(pohyb)
            self.log("som na", self.myself.position,"ideme na", nearest.x, nearest.y)

            update_to = 0
            if len(self.myself.tank.updatable_to)!=0:
                idtan = 10
                for tank in self.myself.tank.updatable_to:
                    if tank.tank_id == 9:
                        idtan = 9
                        break

                update_to = idtan
            else:
                update_to = 0


            return Turn(velocity=pohyb,
                        shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                        stat=random.choice(statynavylep),
                        new_tank_id=update_to)
        


        else:
            if self.myself.position.distance(nearest) < 75:
                if self.myself.health < maxzakladhealth/2:
                    pohyb = self.myself.position
                
                else:
                    pohyb = nearest - self.myself.position
            else:
                pohyb = nearest - self.myself.position


            return Turn(velocity=pohyb,
                        shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                        stat=random.choice(statynavylep),
                        new_tank_id=0)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
