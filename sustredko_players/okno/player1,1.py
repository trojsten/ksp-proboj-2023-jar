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

pozicky = XY(random.randint(-200, 200), random.randint(-200, 200))
zivoty = 3
upgrades = 0
dostal_sa = 0
class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        global zivoty
        global upgrades
        global dostal_sa
        nearest = XY(inf, inf)
        try:
            zivoty +=1
            zivoty -=1
            upgrades += 1
            upgrades -=1
            dostal_sa +=1
            dostal_sa -=1
            
        except:
            self.log("erierbgihberiuhreguihrguihriughiureshgiurebiuerg")
            zivoty = 0
            upgrades = 0
            dostal_sa = 0
            pozicky = XY(0,0)
        if self.myself.lifes_left != zivoty:
            upgrades = 0

        hranica_x = abs(self.world.min_x) + abs(self.world.max_x)
        hranica_y = abs(self.world.min_y) + abs(self.world.max_y)
        hranica_xpol = self.world.min_x + self.world.max_x
        hranica_ypol = self.world.min_y + self.world.max_y
        pozicky = XY((hranica_xpol/2-(hranica_x/4)), (hranica_ypol/2-(hranica_y/4)))
        self.log("pozicia", pozicky, "moja", self.myself.position, "cislo", dostal_sa, "distancia", self.myself.position.distance(pozicky), "hranice", hranica_x, hranica_y, hranica_xpol, hranica_ypol)
        
        

        
        
        if dostal_sa == 1:
            pozicky = XY((hranica_xpol/2+(hranica_x/4)), (hranica_ypol/2-(hranica_y/4)))
        elif dostal_sa == 2:
            pozicky = XY((hranica_xpol/2+(hranica_x/4)), (hranica_ypol/2+(hranica_y/4)))
        elif dostal_sa == 3:
            pozicky = XY((hranica_xpol/2-(hranica_x/4)), (hranica_ypol/2+(hranica_y/4)))
        zivoty = self.myself.lifes_left
        naboj = 0
        pohybo=XY(10,-20)

        if self.myself.position.distance(pozicky) < 6:
            self.log("tubortnounrevubnr", dostal_sa)
            dostal_sa +=1
            self.log("rehuioer", dostal_sa)
            if dostal_sa == 4:
                dostal_sa = 0
        mato = 1
        pozicia_entiti = XY(0,0)
        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                nearest = entity.position
                pozicia_entiti = nearest
                self.log("pozicia jej", pozicia_entiti, "hranice", int((hranica_xpol/2-(hranica_x/3))//1), int((hranica_xpol/2+(hranica_x/3))//1), int((hranica_ypol/2-(hranica_y/3))//1), int((hranica_ypol/2+(hranica_y/3))//1))
        if nearest != XY(inf, inf):
            if dostal_sa == 0:
                if nearest.x < self.myself.position.x:
                    pozicky.x -= hranica_x/10
                if nearest.y < self.myself.position.y:
                    pozicky.y -= hranica_y/10
            elif dostal_sa == 1:
                if nearest.x > self.myself.position.x:
                    pozicky.x += hranica_x /10
                if nearest.y > self.myself.position.y:
                    pozicky.y += hranica_y /10
                if nearest.y < self.myself.position.y:
                    pozicky.y -= hranica_y /10
            elif dostal_sa == 2:
                if nearest.x > self.myself.position.x:
                    pozicky.x += hranica_x /10
                if nearest.y > self.myself.position.y:
                    pozicky.y += hranica_y /10
                if nearest.x < self.myself.position.x:
                    pozicky.x -= hranica_x /10
            elif dostal_sa == 3:
                if nearest.y < self.myself.position.y:
                    pozicky.y -= hranica_y /10
                if nearest.y > self.myself.position.y:
                    pozicky.y += hranica_y /10
                if nearest.x < self.myself.position.x:
                    pozicky.x -= hranica_x /10

        macka = 0
        hracik = 0
        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                macka = 1
                if hracik == 1:
                    if self.myself.position.distance(nearest) > self.myself.position.distance(player.position) and self.myself.position.distance(player.position) < (18*mato):
                        nearest = player.position
                        self.log("lll", self.myself.position.distance(player.position))
                else:
                    nearest = player.position
                hracik = 1
        strely = 0    
        for bulet in self.bullets:
            self.log("naboj", bulet.position, bulet.velocity)
            m1=self.myself.position.angle_to(bulet.position)
            m2=self.myself.position.angle_to(bulet.position+bulet.velocity)
            if self.myself.position.distance(bulet.position) < 70 and self.myself.position.distance(bulet.position) < self.myself.position.distance(bulet.position+bulet.velocity) and bulet.shooter_id != self._myself and m1 > m2-0.2 and m2 > m1-0.2:
                naboj = 1
                pozicky.x += 50
                pozicky.y +=20
        if nearest == XY(inf, inf):
            nearest = pozicky

        
        staka = random.choice((StatsEnum.StatSpeed,StatsEnum.StatRange,StatsEnum.StatRange,StatsEnum.StatHealthMax,StatsEnum.StatHealthRegeneration,StatsEnum.StatReloadSpeed))
        self.log("erinrbegvubergrubrbguergvueru", self.myself.stat_levels[StatsEnum.StatSpeed])
    
        if pozicia_entiti != XY(0,0) and int(pozicia_entiti.x//1) in range(int((hranica_xpol/2-(hranica_x/2.5))//1), int((hranica_xpol/2+(hranica_x/2.5))//1)) and int(pozicia_entiti.y//1) in range(int((hranica_ypol/2-(hranica_y/3))//1), int((hranica_ypol/2+(hranica_y/3))//1)):
            pozicky.x = pozicia_entiti.x + random.randint(50, 80)
            pozicky.y = pozicia_entiti.y + random.randint(50, 80)
            self.log(pozicky, "erbibrehurhurhuuuuuuuuu", pozicia_entiti)
        else:
            pozicky = XY((hranica_xpol/2-(hranica_x/4)), (hranica_ypol/2+(hranica_y/4)))
            if dostal_sa == 1:
                pozicky = XY((hranica_xpol/2+(hranica_x/4)), (hranica_ypol/2-(hranica_y/4)))
            elif dostal_sa == 2:
                pozicky = XY((hranica_xpol/2+(hranica_x/4)), (hranica_ypol/2+(hranica_y/4)))
            elif dostal_sa == 3:
                pozicky = XY((hranica_xpol/2-(hranica_x/4)), (hranica_ypol/2+(hranica_y/4)))

        
        mato = 0
        self.log("strielam na", nearest.x, nearest.y)
        self.log("aaaeee", self.myself.tank.updatable_to, upgrades)
        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice((5,6))
            upgrades +=3
        else:
            update_to = 0
            mato = 0.2
        self.log("jjj", nearest, pozicky)


            
        if self.myself.stat_levels[StatsEnum.StatSpeed] == 0:
            self.log("ziaden naboj", pozicky)
                    
            return Turn(velocity=pozicky - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                    stat=StatsEnum.StatSpeed,
                    new_tank_id=update_to)
        else:
            try:
                self.log("ziaden naboj", pozicky)
                return Turn(velocity=pozicky - self.myself.position,
                        shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                        stat=staka,
                        new_tank_id=update_to)
            except:
                 self.log("ziaden naboj", pozicky)
            return Turn(velocity=XY(random.randint(self.world.min_x, self.world.max_x), random.randint(self.world.min_y, self.world.max_y)) - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                    stat=staka,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
