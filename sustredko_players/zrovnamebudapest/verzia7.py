#!/usr/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

maxzakladhealth = 100
lastlevel = 0
poradieupgr = [0,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatBulletDamage,StatsEnum.StatRange,
               StatsEnum.StatBulletDamage,StatsEnum.StatSpeed,
               StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,StatsEnum.StatSpeed,StatsEnum.StatSpeed,
               StatsEnum.StatSpeed,StatsEnum.StatSpeed,
               StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,
               StatsEnum.StatHealthRegeneration,
               StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,
               StatsEnum.StatSpeed,StatsEnum.StatRange,StatsEnum.StatRange,StatsEnum.StatSpeed,
               StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,StatsEnum.StatBodyDamage,
               StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,StatsEnum.StatHealthRegeneration,
               StatsEnum.StatHealthMax,StatsEnum.StatHealthMax,
               StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed,StatsEnum.StatSpeed]
lastlives = 3
ciel = [500,500]


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class LepsiPlayer(ProbojPlayer):
    
    def make_turn(self) -> Turn:

        global lastlevel,lastlives

        if self.world.min_x != self.world.max_x and self.world.min_y != self.world.max_y:

            ciel = [random.randint(int(self.world.min_x),int(self.world.max_x)),random.randint(int(self.world.min_y),int(self.world.max_y))]

        else:
            ciel = [0,0]
        
        strielam = NoShoot()

        nearest = XY(inf, inf)

        pohyb = XY(ciel[0],ciel[1]) - self.myself.position


        if self.myself.lifes_left < lastlives:
            self.log("""
            preco som skapaaaal

            """)
            lastlevel = 0

        nearestp = None
        
        if self.myself.tank.tank_id != 10:
            for player in self.players.values():
                if player != self.myself:

                    self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                    nearest = player.position
                    nearestp =  player.position
                    strielam = OneBulletShoot(self.myself.position.angle_to(nearest))


        for entity in self.entities:
            if self.myself.tank.tank_id != 10:
                if self.world.min_x < entity.position.x < self.world.max_x and self.world.min_y < entity.position.y < self.world.max_y:
                    if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                        nearest = entity.position
            
            else:
                if self.world.min_x + 100 < entity.position.x < self.world.max_x -100 and self.world.min_y + 100 < entity.position.y < self.world.max_y-100:
                    if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                        nearest = entity.position

        
        
        if self.myself.tank.tank_id == 10:
            for player in self.players.values():
                if player != self.myself and  player.tank.tank_id != 10:

                    self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                    nearest = player.position
                    strielam = OneBulletShoot(self.myself.position.angle_to(nearest))
        

        if nearest.x == inf and nearest.y == inf:
            self.log("idem nkam")
            nearest = XY(ciel[0], ciel[1])
        
        else:
            self.log("nieco vid999999999999m")
        



        

        statynavylep=StatsEnum.StatNone
        if self.myself.level > lastlevel:
            statynavylep = poradieupgr[lastlevel+1]
            lastlevel += 1


        if self.myself.tank.tank_id != 10:


            if self.myself.position.distance(nearest) < 75:
                pohyb = self.myself.position - nearest
                strielam = OneBulletShoot(self.myself.position.angle_to(nearest))


            elif self.myself.position.distance(nearest) < 125:
                if self.myself.reload_cooldown == 0:
                    pohyb = nearest - self.myself.position
                    strielam = OneBulletShoot(self.myself.position.angle_to(nearest))
                else:
                    pohyb = self.myself.position - self.myself.position

            else:
                pohyb = nearest - self.myself.position
            


            if nearestp != None and self.myself.position.distance(nearestp) < 200 or nearest == nearestp:
                pohyb = self.myself.position - nearestp


            
            byvalka = math.inf
            for bulet in self.bullets:
                uholstrely = bulet.position.angle_to(bulet.velocity)
                if byvalka > self.myself.position.distance(bulet.position):
                    
                    if math.pi - uholstrely - math.pi/16 <= self.myself.position.angle_to(bulet.position) <= math.pi - uholstrely + math.pi/16 and bulet.shooter_id != self.myself.id:

                        alpha = self.myself.position.angle_to(nearest)+math.pi/2
                        rychlost = self.myself.stat_values[StatsEnum.StatSpeed]
                        x,y = self.myself.position.x, self.myself.position.y
                        pohyb = XY(x+math.cos(alpha)*rychlost,y+math.sin(alpha)*rychlost) - self.myself.position




            if self.myself.position.x < self.world.min_x + 100:
                pohyb = XY(self.myself.position.x + 100, self.myself.position.y) - self.myself.position
            
            elif self.myself.position.x > self.world.max_x - 100:
                pohyb = XY(self.myself.position.x - 100, self.myself.position.y) - self.myself.position


            if self.myself.position.y < self.world.min_y + 100:
                pohyb = XY(self.myself.position.x, self.myself.position.y + 10) - self.myself.position
            
            elif self.myself.position.y > self.world.max_y - 100:
                pohyb = XY(self.myself.position.x, self.myself.position.y - 10) - self.myself.position
                
                
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
                        shoot=strielam,
                        stat=statynavylep,
                        new_tank_id=update_to)
        


        else:

            if self.myself.position.distance(nearest) < 50:
                pohyb = nearest - self.myself.position
            
            else:
                if self.myself.position.distance(nearest) < 75:
                    if self.myself.health < maxzakladhealth/2:
                        dodge = 1.5
                    else:
                        dodge = 4
                else:
                    dodge = 4

                alpha = self.myself.position.angle_to(nearest)+math.pi/dodge
                rychlost = self.myself.stat_values[StatsEnum.StatSpeed]
                x,y = self.myself.position.x, self.myself.position.y
                pohyb = XY(x+math.cos(alpha)*rychlost,y+math.sin(alpha)*rychlost) - self.myself.position
            

            if self.myself.position.x < self.world.min_x + 20:
                pohyb = XY(self.myself.position.x + 100, self.myself.position.y) - self.myself.position
            
            elif self.myself.position.x > self.world.max_x - 20:
                pohyb = XY(self.myself.position.x - 100, self.myself.position.y) - self.myself.position


            if self.myself.position.y < self.world.min_y + 20:
                pohyb = XY(self.myself.position.x, self.myself.position.y + 100) - self.myself.position
            
            elif self.myself.position.y > self.world.max_y - 20:
                pohyb = XY(self.myself.position.x, self.myself.position.y - 100) - self.myself.position
                
                
                self.log("idem na",pohyb)



            return Turn(velocity=pohyb,
                        shoot=NoShoot(),
                        stat=statynavylep,
                        new_tank_id=0)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
