#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


def norm(v):
    d=math.sqrt(v.x**2+v.y**2)
    return XY(v.x/d, v.y/d)

def size(v):
    return math.sqrt(v.x**2+v.y**2)


class My(ProbojPlayer):
    walk_modes={"Hunting":0,
                "Walking":1,
                "Dodging":2,
                "Centering":3,
                "Edge escape":4}

    shoot_modes={"Hunting":0,
                "Killing":1}

    walk_mode=0
    shoot_mode=0

    entity_avg=2
    

    player_last_positions=dict()
    
    last_turn=Turn(XY(0, 0), NoShoot(), StatsEnum.StatNone, 0)

    def make_turn(self) -> Turn:
        players=self.players.values()
        entities=self.entities
        bullets=self.bullets
        wsx=self.world.min_x-self.world.max_x
        wsy=self.world.min_y-self.world.max_y

        near_edge=False
        if self.myself.position.x+wsx/6 > self.world.max_x or self.myself.position.x-wsx/6 < self.world.min_x or self.myself.position.y+wsx/6 > self.world.max_y or self.myself.position.y-wsx/6 < self.world.min_y:
            near_edge=True
        if (self.myself.position.x+self.myself.stat_values[StatsEnum.StatBulletSpeed]*4 > self.world.max_x or
                self.myself.position.x-self.myself.stat_values[StatsEnum.StatBulletSpeed]*2 < self.world.min_x or
                self.myself.position.y+self.myself.stat_values[StatsEnum.StatBulletSpeed]*2 > self.world.max_y or
                self.myself.position.y-self.myself.stat_values[StatsEnum.StatBulletSpeed]*2 < self.world.min_y):
            self.walk_mode=3
        elif len(self.entities)>0:
            self.walk_mode=0
        else:
            self.walk_mode=1
        


        nearest = XY(inf, inf)
        nearest_bullet_time=inf
        nearest_is_player=False

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                    if not player.id in self.player_last_positions:
                        velocity=XY(0, 0)
                    else:
                        velocity=player.position-self.player_last_positions[player.id]
                    
                    nearest = player.position+(self.myself.position.distance(player.position)/self.myself.stat_values[StatsEnum.StatBulletSpeed])*velocity
                    nearest_is_player = True

            self.player_last_positions[player.id]=player.position
                    
                        
        if not nearest_is_player:
            for entity in self.entities:
                if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                    nearest = entity.position
        

        

        for bullet in self.bullets:
            if bullet.shooter_id != self.myself.id:
                bullet_path=Segment(bullet.position, bullet.position+bullet.velocity*bullet.ttl)
                bullet_path_distance=Segment.segment_point_distance(bullet_path, self.myself.position)
                if bullet_path_distance<self.myself.radius + bullet.radius + 3*self.myself.stat_values[StatsEnum.StatSpeed]:
                    self.walk_mode=2
                    bullet_time=self.myself.position.distance(bullet.position)/size(bullet.velocity)
                    if bullet_time < nearest_bullet_time:
                        nearest_bullet_time=bullet_time
                        nearest_bullet_path=bullet_path
                        nearest_bullet=bullet

        if self.myself.position.x > self.world.max_x or self.myself.position.x < self.world.min_x or self.myself.position.y > self.world.max_y or self.myself.position.y < self.world.min_y:
            self.walk_mode=3

        if self.walk_mode==0:
            if nearest_is_player:
                ideal_dist=min(self.myself.stat_values[StatsEnum.StatRange], self.myself.stat_values[StatsEnum.StatBulletTTL]*self.myself.stat_values[StatsEnum.StatBulletSpeed])-100
            else:
                ideal_dist=100
            if self.myself.position.distance(nearest) > ideal_dist:
                move_target=nearest
            else:
                move_target=self.myself.position+self.myself.position-nearest
                
        elif self.walk_mode==1:
            center=XY((self.world.min_x+self.world.max_x)/2, (self.world.min_y+self.world.max_y)/2)
            if self.myself.position.distance(center)>min(self.world.max_x - self.world.min_x, self.world.max_y - self.world.min_y)/4:
                if self.myself.position.x>center.x:
                    y=self.world.max_y
                else:
                    y=self.world.min_y
                if self.myself.position.y<center.y:
                    x=self.world.max_x
                else:
                    x=self.world.min_x
                move_target=XY(x, y)
            else:
                move_target = self.myself.position+self.myself.position-center
                
        elif self.walk_mode==2:
            dodge_direction=XY(nearest_bullet.velocity.y, nearest_bullet.velocity.x*-1)
            if Segment.segment_point_distance(nearest_bullet_path, self.myself.position+dodge_direction) < Segment.segment_point_distance(nearest_bullet_path, self.myself.position-dodge_direction):
                move_target=self.myself.position-dodge_direction
            else:
                move_target=self.myself.position+dodge_direction
                
        elif self.walk_mode==3:
            move_target=XY((self.world.min_x+self.world.max_x)/2, (self.world.min_y+self.world.max_y)/2)
            
        if near_edge and self.walk_mode != 2:
            move_target = 0.5*(move_target+XY((self.world.min_x+self.world.max_x)/2, (self.world.min_y+self.world.max_y)/2))

        self.entity_avg*=0.95
        self.entity_avg += len(self.entities)/20+(len(self.players)-1)/2
        self.log(self.entity_avg)
        if self.entity_avg >= 1.5:
            if self.myself.stat_levels[StatsEnum.StatReloadSpeed] <= self.myself.stat_levels[StatsEnum.StatBulletDamage]-1:
                stat=StatsEnum.StatReloadSpeed
            elif self.myself.stat_levels[StatsEnum.StatBulletDamage] <= self.myself.stat_levels[StatsEnum.StatHealthRegeneration]:
                stat=StatsEnum.StatBulletDamage
            elif self.myself.stat_levels[StatsEnum.StatHealthRegeneration] <= self.myself.stat_levels[StatsEnum.StatBulletTTL]-1:
                stat=StatsEnum.StatHealthRegeneration
            else:
                stat=StatsEnum.StatBulletTTL
        else:
            if self.myself.stat_levels[StatsEnum.StatSpeed] <= self.myself.stat_levels[StatsEnum.StatRange] - 3:
                stat=StatsEnum.StatSpeed
            else:
                stat=StatsEnum.StatRange
                
            

        return Turn(move_target-self.myself.position, OneBulletShoot(self.myself.position.angle_to(nearest)), stat, 5)
        

















    

if __name__ == "__main__":
    p = My()
    p.run()



    
