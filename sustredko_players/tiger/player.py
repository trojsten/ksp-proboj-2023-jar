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

class moje(ProbojPlayer):
    #global velocity
    def make_turn(self) -> Turn:
        #global velocity,upgrady_index, predosly_level, tah
        nearest_entity = XY(inf, inf)
        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest_entity):
                nearest_entity = entity.position
        if nearest_entity == XY(inf, inf):
            nearest_entity = XY(0, 0)

        # self.log("bu1")

        nearest_player = XY(inf, inf)
        for player in self.players.values():
            if player != self.myself:
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_player):
                    nearest_player = player.position
        if nearest_player == XY(inf, inf):
            nearest_player = XY(0, 0)

        if self.myself.position.distance(nearest_entity) >= self.myself.position.distance(nearest_player):
            nearest = nearest_player
        else:
            nearest = nearest_entity


        target = XY(0,0)
        if nearest_entity != XY(inf,inf):
            target = nearest_entity
        if nearest_player != XY(inf,inf):
            target = nearest_player
        # self.log("bu2")

        # self.log(self._read_bullets())

        # self.log("bu2.25")

        # nearest_bullet = XY(inf,inf)
        # for bullet in self._read_bullets():
        #     self.log("bu2.5")
        #     if self.myself.position.distance(bullet.position) < self.myself.position.distance(nearest_bullet):
        #         nearest_bullet = bullet.position

        # self.log("bu3")

        # if nearest_bullet != XY(inf,inf):
        #     v = nearest_bullet.velocity
        #     velocity = XY(-v.y,v.x)*1000# + self.myself.position
        # else:
        
        # if random.randint(0, 40) == 1:
        #     velocity = XY(random.randint(0, 1000), random.randint(0, 1000))# - self.myself.position
            # self.log(velocity, "rychlost")
        if nearest == XY(inf, inf):
            nearest = XY(0, 0)
        velocity = nearest - self.myself.position
        #if self.myself.position.distance(nearest) < 20:
        #    velocity = XY(0,0)

        # if self.world.max_x < self.myself.position.x + 50:
        #     velocity = XY(-1000,0)
        # if self.world.max_y < self.myself.position.y + 50:
        #     velocity = XY(0,-1000)
        # if self.world.min_x > self.myself.position.x - 50:
        #     velocity = XY(1000,0)
        # if self.world.min_y > self.myself.position.y - 50:
        #     velocity = XY(1000,0)
        
        # moznosti_upgradov = [StatsEnum.StatNone,StatsEnum.StatRange,StatsEnum.StatSpeed,StatsEnum.StatBulletSpeed,StatsEnum.StatBulletTTL,StatsEnum.StatBulletDamage,StatsEnum.StatHealthMax,StatsEnum.StatHealthRegeneration,StatsEnum.StatBodyDamage,StatsEnum.StatReloadSpeed]
        # upgrady = [StatsEnum.StatBulletTTL,StatsEnum.StatBulletTTL,StatsEnum.StatBulletTTL,StatsEnum.StatBulletTTL,StatsEnum.StatBulletDamage,StatsEnum.StatBulletDamage,StatsEnum.StatBulletDamage,StatsEnum.StatBulletDamage]
        #stat_upgrade = 0
        # if self.myself.level > predosly_level:
        #     stat_upgrade = upgrady[self.myself.level]

        # predosly_level = self.myself.level
        #tah += 1
        # if tah > 10:
        #velocity = XY(1000,0)
        return Turn(velocity=velocity,
                    shoot=OneBulletShoot(self.myself.position.angle_to(target)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=random.choice((5,8)))

class moje2(ProbojPlayer):
    def make_turn(self) -> Turn:
        # self.log("bu")
        try:
            a = self.velocity
            a = self.predosly_level
            a = self.tah
            a = self.upgrade_index
        except:
            self.velocity = XY(1000,0)
            self.predosly_level = -1
            self.tah = 0
            self.upgrade_index = 0
            self.dodge_velocity = XY(0,0)



        nearest = XY(inf, inf)
        nearest_player = XY(inf, inf)
        nearest_entity = XY(inf, inf)
        vidimedakoho = False
        vidimeplayer = False
        vidimeentity = False
        self.log("tah",self.tah)
        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest_entity):
                nearest_entity = entity.position
                vidimedakoho = True
                vidimeentity = True

        self.log("bu")

        for player in self.players.values():
            if player != self.myself:
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_player):
                    nearest_player = player.position
                    vidimedakoho = True
                    vidimeplayer = True

        nearest_bullet = XY(inf,inf)
        for bullet in self.bullets:
            if self.myself.position.distance(bullet.position) < self.myself.position.distance(nearest_bullet):
                nearest_bullet = bullet.position

        target = -1
        if vidimeentity:
            target = nearest_entity
        if vidimeplayer:
            target = nearest_player

        if not vidimedakoho:
            # self.log("bu1")
            #nearest = XY(0, 0)
            # if self.tah%40 == 0:
            #     self.velocity = XY(random.randint(0, 1000), random.randint(0, 1000))# - self.myself.position
            self.velocity = XY((self.world.max_x-self.world.min_x)/2, (self.world.max_y-self.world.min_y)/2) - self.myself.position
        else:
            if vidimeentity:
                self.velocity = nearest_entity - self.myself.position
                #if self.myself.tank.tank_id() != 10:
                if self.myself.position.distance(nearest_entity) < 100:
                    self.velocity = XY(0,0)
            else:
                 self.velocity = XY(0,0)

        pri_okraji = False
        min_rozdiel = inf
        okraj = 120
        if self.world.max_x < self.myself.position.x + okraj:
            self.velocity = XY(-1000,0)
            min_rozdiel = abs(self.world.max_x - self.myself.position.x)
            pri_okraji = True
        if self.world.max_y < self.myself.position.y + okraj and abs(self.world.max_y - self.myself.position.y) < min_rozdiel:
            self.velocity = XY(0,-1000)
            min_rozdiel = abs(self.world.max_y - self.myself.position.y)
            pri_okraji = True
        if self.world.min_x > self.myself.position.x - okraj and abs(self.world.min_x - self.myself.position.x) < min_rozdiel:
            self.velocity = XY(1000,0)
            min_rozdiel = abs(self.world.min_x - self.myself.position.x)
            pri_okraji = True
        if self.world.min_y > self.myself.position.y - okraj and abs(self.world.min_y - self.myself.position.y) < min_rozdiel:
            self.velocity = XY(0,1000)
            pri_okraji = True
        if pri_okraji:
            target = XY(-self.velocity.x,-self.velocity.y)+self.myself.position



        # self.log("bu")
        moznosti_upgradov = [StatsEnum.StatNone,StatsEnum.StatRange,StatsEnum.StatSpeed,StatsEnum.StatBulletSpeed,StatsEnum.StatBulletTTL,StatsEnum.StatBulletDamage,StatsEnum.StatHealthMax,StatsEnum.StatHealthRegeneration,StatsEnum.StatBodyDamage,StatsEnum.StatReloadSpeed]
        upgrady = [5,2,5,2,9,2,5,9,5,9,5,9,5,9,5,9,5,9,9,8,8,8,8,8,8,8]#[5,2,5,2,5,2,3,4,1,3,4,1,3,4,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1]
        #[3,4,5,1,3,4,5,1,3,2,2,2,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1]
        #[3,4,5,1]*20#[3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5]
        #[8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6,8,7,2,6]#[1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]
        stat_upgrade = StatsEnum.StatNone
        if self.myself.level > self.predosly_level:
            stat_upgrade = moznosti_upgradov[upgrady[self.upgrade_index]]
            self.upgrade_index += 1


        # self.log("bub")
        # if target == -1:
        #     target = XY(-self.velocity.x,-self.velocity.y)
        # self.log("bub")


        if target == -1:
            strela = NoShoot()
        else:
            rozsah = 15#stupnov
            strela = OneBulletShoot(self.myself.position.angle_to(target) + (2*math.pi/360)*random.randint(-rozsah*1000, rozsah*1000)/1000)#+- 2pi/360*10
            


        if self.velocity.x == 0 and self.velocity.y == 0:# and self.myself.position.distance(nearest_bullet) < 600:
            #g = nearest_bullet - self.myself.position
            if self.tah%15 == 0:
                self.dodge_velocity = XY(random.randint(-1000, 1000)*1000, random.randint(-1000, 1000)*1000)
                self.log(self.dodge_velocity,"dv")
            self.velocity = self.dodge_velocity
            #XY(-g.y,g.x)*1000#random.choice((XY(-g.y,g.x), XY(g.y,-g.x)))


        self.tah += 1
        self.predosly_level = self.myself.level
        # self.log("bu",self.velocity)
        return Turn(velocity=self.velocity,
                    shoot=strela,
                    stat=stat_upgrade,
                    new_tank_id=random.choice((5,6)))#9,10 peaceful


if __name__ == "__main__":
    p = moje2()
    p.run()



        # self.log("ideme na", nearest.x, nearest.y)

        # if len(self.myself.tank.updatable_to)!=0:
        #     update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        # else:
        #     update_to = 0

# StatNone = 0
# StatRange = 1
# StatSpeed = 2
# StatBulletSpeed = 3
# StatBulletTTL = 4
# StatBulletDamage = 5
# StatHealthMax = 6
# StatHealthRegeneration = 7
# StatBodyDamage = 8
# StatReloadSpeed = 9
