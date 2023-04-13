#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
from libs.stats import *
import libs.stats as stats

#todo pridat staty
constup = [
    [9,StatsEnum.StatRange],
    [6,StatsEnum.StatSpeed],
    [7,StatsEnum.StatBulletDamage],
    [9,StatsEnum.StatBulletSpeed],
    [9,StatsEnum.StatBulletTTL],
    [10,StatsEnum.StatReloadSpeed],
    [1,StatsEnum.StatHealthMax],
    [1,StatsEnum.StatHealthRegeneration],
    [0,StatsEnum.StatBodyDamage]






]
global prio
prio = []
class MyPlayer(ProbojPlayer):


    def make_turn(self) -> Turn:
        #defines
        if self.myself.stat_values[StatsEnum.StatReloadSpeed] < 2:
                for j in range(1999):
                    prio.append(StatsEnum.StatReloadSpeed)
        if self.myself.stat_values[StatsEnum.StatSpeed] < 2:
            for j in range(999):
                prio.append(StatsEnum.StatSpeed)


        if self.myself.stat_values[StatsEnum.StatBulletDamage] < 2:
                for j in range(999):
                    prio.append(StatsEnum.StatBulletDamage)

        for i in constup:
            if self.myself.stat_values[StatsEnum.StatSpeed] >=7:
                continue
            for j in range(i[0]):
                prio.append(i[1])

        def je_v_mape(pos):
            if pos.x > self.world.max_x or pos.x < self.world.min_x or pos.y > self.world.max_y or  pos.y <self.world.min_y:
                return False
            else:
                return True

        def mam_range(enemy):
            if self.myself.stat_values[StatsEnum.StatBulletTTL] * self.myself.stat_values[
                StatsEnum.StatBulletSpeed] > self.myself.position.distance(enemy):
                return True
            else:
                return False

        #todo utekanie ???


        #blok na pohyb

        def pohyb():

            nearestPlayer = XY(inf, inf)
            for player in self.players.values():
                if player != self.myself:
                    if self.myself.position.distance(player.position) < self.myself.position.distance(nearestPlayer):
                        nearestPlayer = player.position



            nearest = XY(inf, inf)

            for entity in self.entities:
                if je_v_mape(entity.position):
                    if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                        if self.myself.position.distance(entity.position) < self.myself.radius + self.myself.stat_values[
                            StatsEnum.StatSpeed] + entity.radius +50:
                            pass
                        else:
                            nearest = entity.position


            #todo maybe neskor


            #strilanie je prio na hracov





            x = self.myself.position.x
            y = self.myself.position.y





            #hopefully toto bude fungovat

            if self.world.min_x > x or self.world.max_x < x or self.world.max_y < y or  self.world.min_y > y:
                nearest.x = (self.world.max_x+self.world.min_x)/2
                nearest.y = (self.world.max_y+self.world.min_y)/2

            if nearest == self.myself.position or nearest.x ==inf:
                nearest.x = ((self.world.max_x + self.world.min_x) / 2)
                nearest.y = ((self.world.max_y + self.world.min_y) / 2)





            # ak by nastala zrazka
            #todo radius entitiy a mozno knowckback zo strely

            if (nearest == self.myself.position or nearest.x ==inf) and nearestPlayer != XY(inf, inf):
                return nearestPlayer
            return nearest

        nearest = pohyb()


        #todo priblizuj dokym mas range lae prio na entity
        def strielaj():
            target = XY(inf,inf)
            targetPlayer = XY(inf,inf)

            for entity in self.entities:
                if self.myself.position.distance(entity.position) < self.myself.position.distance(target):
                    target = entity.position


            for player in self.players.values():
                if player != self.myself:
                    if self.myself.position.distance(player.position) < self.myself.position.distance(targetPlayer):
                        targetPlayer = player.position

            if mam_range(targetPlayer):
                return targetPlayer
            else:
                return target


        target = strielaj()




        if len(self.myself.tank.updatable_to) != 0:
            #update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
            update_to = [tank.tank_id for tank in self.myself.tank.updatable_to][len(self.myself.tank.updatable_to)-1]
        else:
            update_to = 0

        if nearest == self.myself.position or nearest.x ==inf:
            nearest= (((self.world.max_x + self.world.min_x) / 2),((self.world.max_y + self.world.min_y) / 2))

        return Turn(velocity=nearest - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(target)),
                    stat=random.choice(prio),
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
