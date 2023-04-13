#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
tiktak = 0
class MojPlayer(ProbojPlayer):
    tiktak += 1
    def make_turn(self) -> Turn:
        go_pos = XY(inf, inf)
        shoot_pos = XY(inf,inf)
        bullet_pos = XY(inf,inf)

        for bullet in self.bullets:
            if bullet.shooter_id != self.myself.id:
                if self.myself.position.distance(bullet.position) < self.myself.position.distance(bullet_pos):
                    bullet_pos = bullet.position

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(shoot_pos):
                shoot_pos = entity.position
        
        player_shoot_pos = XY(inf,inf)
        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(player_shoot_pos):
                    player_shoot_pos = player.position
                    shoot_pos = player.position

        update_to = 0
        if self.myself.tank.tank_id == BasicTank.tank_id:
            update_to = SniperTank.tank_id
       
        if self.myself.tank.tank_id == SniperTank.tank_id:
            update_to = WideBulletTank.tank_id
        
        level_up = StatsEnum.StatNone        
        if self.myself.stat_levels[StatsEnum.StatSpeed] < 3:
            level_up = StatsEnum.StatSpeed
        elif self.myself.stat_levels[StatsEnum.StatBulletTTL] < 3:
            level_up = StatsEnum.StatBulletTTL
        elif self.myself.stat_levels[StatsEnum.StatBulletDamage] < 7:
            level_up = StatsEnum.StatBulletDamage
        elif self.myself.stat_levels[StatsEnum.StatRange] < 7:
            level_up = StatsEnum.StatRange
        elif self.myself.stat_levels[StatsEnum.StatBulletTTL] < 7:
            level_up = StatsEnum.StatBulletTTL
        elif self.myself.stat_levels[StatsEnum.StatSpeed] < 7:
            level_up = StatsEnum.StatSpeed
        elif self.myself.stat_levels[StatsEnum.StatHealthRegeneration] < 7:
            level_up = StatsEnum.StatHealthRegeneration
        elif self.myself.stat_levels[StatsEnum.StatHealthMax] < 7:
            level_up = StatsEnum.StatHealthMax 
        elif self.myself.stat_levels[StatsEnum.StatReloadSpeed] < 7:
            level_up = StatsEnum.StatReloadSpeed
        elif self.myself.stat_levels[StatsEnum.StatBulletSpeed] < 7:
            level_up = StatsEnum.StatBulletSpeed
        elif self.myself.stat_levels[StatsEnum.StatBodyDamage] < 7:
            level_up = StatsEnum.StatBodyDamage

        wait_pos = XY(inf, inf)
        wait_dist = XY(inf,inf)
        if (shoot_pos.x == inf and shoot_pos.y == inf):
            
            if (self.myself.position.y - self.world.min_y <= self.world.max_y - self.myself.position.y):
                wait_pos.y = self.world.min_y + 200
                wait_dist.y = self.myself.position.y - self.world.min_y
            else: 
                wait_pos.y = self.world.max_y - 200
                wait_dist.y = self.world.max_y - self.myself.position.y
            if(self.myself.position.x - self.world.min_x <= self.world.max_x - self.myself.position.x):
                wait_pos.x = self.world.min_x + 200
                wait_dist.x = self.myself.position.x - self.world.min_x
            else: 
                wait_pos.x = self.world.max_x - 200
                wait_dist.x = self.world.max_x - self.myself.position.x

            if (wait_pos.x <= wait_pos.y):
                go_pos.x = wait_pos.x
                go_pos.y = self.myself.position.y + 10
            else:
                go_pos.x = self.myself.position.x + 10
                go_pos.y = wait_pos.y
        else:
            if self.myself.tank.tank_id == BasicTank.tank_id:
                stayr = 100
            elif self.myself.tank.tank_id == SniperTank.tank_id:
                stayr = 100 + 200 * self.myself.stat_levels[StatsEnum.StatBulletTTL]
            else: 
                stayr = 50 + 120 * self.myself.stat_levels[StatsEnum.StatBulletTTL]
            if (self.myself.position.x >= shoot_pos.x):
                go_pos.x = shoot_pos.x+stayr
            else:
                go_pos.x = shoot_pos.x-stayr
            
            if (self.myself.position.y >= shoot_pos.y):
                go_pos.y = shoot_pos.y+stayr
            else:
                go_pos.y = shoot_pos.y-stayr
        
        if tiktak < 800:
            borderr = 100
        else:
            borderr = 200
        self.log("world min x y", self.world.min_x, self.world.min_y)
        self.log("world max x y", self.world.max_x, self.world.max_y)
        if self.world.max_x * 2 < 700:
            if (go_pos.y < self.world.min_y + borderr/2):
                go_pos.y = self.world.min_y + borderr/2
            if (go_pos.y > self.world.max_y-borderr/2):
                go_pos.y = self.world.max_y - borderr/2
            if (go_pos.x < self.world.min_x + borderr/2):
                go_pos.x = self.world.min_x + borderr/2
            if (go_pos.x > self.world.max_x - borderr/2):
                go_pos.x = self.world.max_x - borderr/2
        else:  
            if (go_pos.y < self.world.min_y + borderr):
                go_pos.y = self.world.min_y + borderr
            if (go_pos.y > self.world.max_y-borderr):
                go_pos.y = self.world.max_y - borderr
            if (go_pos.x < self.world.min_x + borderr):
                go_pos.x = self.world.min_x + borderr
            if (go_pos.x > self.world.max_x - borderr):
                go_pos.x = self.world.max_x - borderr
            if tiktak > 800:
                if (go_pos.y < self.world.min_y + borderr*1.5):
                    shoot_pos.x = inf
                    shoot_pos.y = inf
                if (go_pos.y > self.world.max_y-borderr*1.5):
                    shoot_pos.x = inf
                    shoot_pos.y = inf
                if (go_pos.x < self.world.min_x + borderr*1.5):
                    shoot_pos.x = inf
                    shoot_pos.y = inf
                if (go_pos.x > self.world.max_x - borderr*1.5):
                    shoot_pos.x = inf
                    shoot_pos.y = inf
            
        
        if shoot_pos.x == inf and shoot_pos.y == inf and bullet_pos.x != inf:
            shoot_pos.x = bullet_pos.x
            shoot_pos.y = bullet_pos.y
            go_pos.x = bullet_pos.x * 0.5
            go_pos.y = bullet_pos.y

        self.log("som na", self.myself.position.x, self.myself.position.y)
        self.log("ideme na", go_pos.x, go_pos.y)
        self.log("strielam na", shoot_pos.x, shoot_pos.y)
        self.log("updatujem ", level_up)
        self.log("bullet_pos", bullet_pos.x, bullet_pos.y)

        if shoot_pos.x != inf and shoot_pos.y != inf:
            return Turn(velocity=go_pos - self.myself.position,
                        shoot=OneBulletShoot(self.myself.position.angle_to(shoot_pos)),
                        stat=level_up,
                        new_tank_id=update_to)
        else:
            return Turn(velocity=go_pos - self.myself.position,
                        shoot=NoShoot(),
                        stat=level_up,
                        new_tank_id=update_to)


if __name__ == "__main__":
    p = MojPlayer()
    p.run()
