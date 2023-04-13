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
    def far_from_border(object, min_x, max_x, min_y, max_y):
        if abs(object.position.x-min_x) > 100 and abs(object.position.x-max_x) > 100 and abs(object.position.y-max_y) > 100 and\
        abs(object.position.y-min_y) > 100:
            return True
        return False
    
    def make_turn(self) -> Turn:
        nearest_entity = XY(inf, inf)
        nearest_enemy = XY(inf, inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest_entity):
                nearest_entity = entity.position

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_enemy):
                    nearest_enemy = player.position

            
        move_to = XY(0, 0)
        shoot_to = XY(0, 0)
            
        move_to = nearest_entity
        shoot_to = nearest_entity
        
        if nearest_enemy != XY(inf, inf):
            shoot_to = nearest_enemy
            
        if move_to.x == inf and move_to.y == inf:
            down, right = True, True
            if self.myself.position.x < 0:
                right = False
            if self.myself.position.y < 0:
                down = False
            if right and down:
                move_to = XY(10+self.myself.position.x , 10+self.myself.position.y)
            elif right and not down:
                move_to = XY(10+self.myself.position.x, -10+self.myself.position.y)
            elif not right and down:
                move_to = XY(-10+self.myself.position.x, 10+self.myself.position.y)
            elif not right and not down:
                move_to = XY(-10+self.myself.position.x, -10+self.myself.position.y)
            self.log(move_to)
        
        if min(abs(self.myself.position.x - self.world.min_x), abs(self.myself.position.x - self.world.max_x), abs(self.myself.position.y - self.world.min_y),\
            abs(self.myself.position.y - self.world.max_y)) < 170:
            if abs(self.myself.position.x - self.world.min_x) < abs(self.myself.position.x - self.world.max_x) and\
                abs(self.myself.position.x - self.world.min_x) < abs(self.myself.position.y - self.world.min_y) and\
                abs(self.myself.position.x - self.world.min_x) < abs(self.myself.position.y - self.world.max_y):
                move_to = XY(self.myself.position.x+200, self.myself.position.y)
            elif abs(self.myself.position.x - self.world.max_x) < abs(self.myself.position.x - self.world.min_x) and\
                abs(self.myself.position.x - self.world.max_x) < abs(self.myself.position.y - self.world.min_y) and\
                abs(self.myself.position.x - self.world.max_x) < abs(self.myself.position.y - self.world.max_y):
                move_to = XY(self.myself.position.x-200, self.myself.position.y)
            elif abs(self.myself.position.y - self.world.max_y) < abs(self.myself.position.x - self.world.min_x) and\
                abs(self.myself.position.y - self.world.max_y) < abs(self.myself.position.y - self.world.min_y) and\
                abs(self.myself.position.y - self.world.max_y) < abs(self.myself.position.x - self.world.max_x):
                move_to = XY(self.myself.position.x, self.myself.position.y-200)
            elif abs(self.myself.position.y - self.world.min_y) < abs(self.myself.position.x - self.world.min_x) and\
                abs(self.myself.position.y - self.world.min_y) < abs(self.myself.position.y - self.world.max_y) and\
                abs(self.myself.position.y - self.world.min_y) < abs(self.myself.position.x - self.world.max_x):
                move_to = XY(self.myself.position.x, self.myself.position.y+200)
                    
                    
        
            
        #if move_to == XY(inf, inf):
        #    move_to = XY((-self.myself.position.x), (-self.myself.position.y))
        
            
        level_up = StatsEnum.StatNone
        if self.myself.stat_levels[StatsEnum.StatBulletDamage] < 4:
            level_up = StatsEnum.StatBulletDamage
        elif self.myself.stat_levels[StatsEnum.StatRange] < 4:
            level_up = StatsEnum.StatRange
        elif self.myself.stat_levels[StatsEnum.StatSpeed] < 3:
            level_up = StatsEnum.StatSpeed
        elif self.myself.stat_levels[StatsEnum.StatReloadSpeed] < 4:
            level_up = StatsEnum.StatReloadSpeed
        elif self.myself.stat_levels[StatsEnum.StatRange] < 7:
            level_up = StatsEnum.StatRange
        elif self.myself.stat_levels[StatsEnum.StatBulletDamage] < 7:
            level_up = StatsEnum.StatBulletDamage
        elif self.myself.stat_levels[StatsEnum.StatBulletTTL] < 7:
            level_up = StatsEnum.StatBulletTTL
        elif self.myself.stat_levels[StatsEnum.StatReloadSpeed] < 7:
            level_up = StatsEnum.StatReloadSpeed
        elif self.myself.stat_levels[StatsEnum.StatBulletSpeed] < 7:
            level_up = StatsEnum.StatBulletSpeed
        elif self.myself.stat_levels[StatsEnum.StatHealthMax] < 7:
            level_up = StatsEnum.StatHealthMax
        elif self.myself.stat_levels[StatsEnum.StatHealthRegeneration] < 7:
            level_up = StatsEnum.StatHealthRegeneration
        elif self.myself.stat_levels[StatsEnum.StatBodyDamage] < 7:
            level_up = StatsEnum.StatBodyDamage

        update_to = 5
        if len(self.myself.tank.updatable_to)!=0:
            #if 7 in [tank.tank_id for tank in self.myself.tank.updatable_to] and self.myself.stat_levels[StatsEnum.StatBulletTTL] > 5:
            #    update_to = 7
            if 5 in [tank.tank_id for tank in self.myself.tank.updatable_to]:
                update_to = 5
        else:
            update_to = 0
        
        
        
        
            
        if shoot_to == XY(inf, inf):
            shoot_to = XY(100, 100)
        
        self.log(move_to)
        
        return Turn(velocity=move_to - self.myself.position,
                    shoot=OneBulletShoot(self.myself.position.angle_to(shoot_to)),
                    stat=level_up,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
