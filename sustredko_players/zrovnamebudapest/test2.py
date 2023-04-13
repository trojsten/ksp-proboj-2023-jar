#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

utec_smerom = False
orientacny_beh = XY(0, 0)
a_dost = True

class MyPlayer(ProbojPlayer):

    def make_turn(self) -> Turn:
        global utec_smerom, orientacny_beh, a_dost
        nearest = XY(inf, inf)

        '''
        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                    orientacny_beh = player.position
                    self.log('nic                    ', orientacny_beh)
        
        if a_dost:
            for bullet in self.bullets:

                moj_uhlik_k_strele = self.myself.position.angle_to(bullet.position)
                uhlik_ktorym_ide_strela = bullet.position.angle_to(bullet.velocity)
                

                self.log('ideeeeeeecko   ', bullet.shooter_id)
                self.log('uhololololo                      ', uhlik_ktorym_ide_strela)

                if bullet.shooter_id != 1:
                    if bullet.position.angle_to(bullet.velocity) == moj_uhlik_k_strele or True:
                        
                        
                        self.log('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ davaj pozor')

                        orientacny_beh = XY(self.myself.position.x+math.cos(uhlik_ktorym_ide_strela+math.pi)*1000,           self.myself.position.y+math.sin(uhlik_ktorym_ide_strela)*1000)
                        a_dost = False


                        self.log('boddddddddddddddddddddddd >              ', orientacny_beh)

                self.log('uhli sa >  ', uhlik_ktorym_ide_strela)
                self.log('dobre', self.myself.position.angle_to(nearest))
        '''
            



        if utec_smerom == False or True:
            nearest = XY(0, 0)

        return Turn(velocity=orientacny_beh - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(orientacny_beh)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)































class LepsiPlayer(ProbojPlayer):

    
    def make_turn(self) -> Turn:
        global utec_smerom
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
        skalarny_dostrel = ''
        for bullet in self.bullets:
            
            ttl = bullet.ttl
            skalarny_dostrel = ttl * self.myself.position.distance(bullet.position)

            moj_uhlik_k_strele = self.myself.position.angle_to(bullet.position)
            uhlik_ktorym_ide_strela = bullet.position.angle_to(bullet.velocity)
            

            self.log('ideeeeeeecko   ', bullet.shooter_id)
            if bullet.shooter_id != 1:
                if bullet.position.angle_to(bullet.velocity) == moj_uhlik_k_strele:
                    self.log('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                    utec_smerom = uhlik_ktorym_ide_strela - 3.14
                    self.log('utekaaaaaaaaaaaaaaaaaaaaaj  ', utec_smerom)

                    bod_uteku = XY(bullet.position.y, -bullet.position.x)


                    self.log('boddddddddddddddddddddddd >              ', bod_uteku)
            self.log('uhli sa >  ', uhlik_ktorym_ide_strela)
            self.log('dobre', self.myself.position.angle_to(nearest))
            
            



        if utec_smerom == False or True:
            nearest = XY(0, 0)




        if len(self.myself.tank.updatable_to)!=0:
            update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0



        return Turn(velocity=bod_uteku - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(nearest)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
