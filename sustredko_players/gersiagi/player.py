#!/usr/bin/env python3
from math import inf
import random

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class Hrac(ProbojPlayer):
    EDGE_PADDING = 100
    next_target = None
    last_pos = None

    def random_position(self, center):
        if self.world.min_x + self.EDGE_PADDING >= self.world.max_x - self.EDGE_PADDING or \
           self.world.min_y + self.EDGE_PADDING >= self.world.max_y - self.EDGE_PADDING:
            return center
        return XY(random.randint(self.world.min_x + self.EDGE_PADDING, self.world.max_x - self.EDGE_PADDING),
                  random.randint(self.world.min_y + self.EDGE_PADDING, self.world.max_y - self.EDGE_PADDING))
    
    def is_inside(self, pos):
        return self.world.min_x < pos.x < self.world.max_x and self.world.min_y < pos.y < self.world.max_y  
    

    upgrades = 0
    stat_upgrade_order = [
        StatsEnum.StatHealthRegeneration,
        StatsEnum.StatBulletDamage,
        StatsEnum.StatBulletDamage,
        StatsEnum.StatHealthMax,
        StatsEnum.StatSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletDamage,
        StatsEnum.StatHealthRegeneration,
        StatsEnum.StatReloadSpeed, # tank upgrade -> sniper
        StatsEnum.StatHealthMax,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed, # tank upgrade -> wide bullet
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBulletSpeed,
    ]

    def do_upgrade(self):
        obj = None
        if len(self.stat_upgrade_order) <= self.upgrades:
            obj = random.choice([2, 3, 4, 5, 5, 6, 7, 9])
        else:
            obj = self.stat_upgrade_order[self.upgrades]
        self.upgrades += 1
        return obj

    def do_tank_update(self):
        if self.myself.tank.tank_id == BasicTank().tank_id:
            return SniperTank().tank_id
        elif self.myself.tank.tank_id == SniperTank().tank_id:
            return WideBulletTank().tank_id 
    
    
    def towards(self, pos: XY):
        return XY(pos.x - self.myself.position.x, pos.y - self.myself.position.y)


    def make_turn(self) -> Turn:
        shoot = NoShoot()
        move = XY(0, 0)
        stat = StatsEnum.StatNone
        new_tank = None

        center = XY((self.world.min_x+self.world.max_x)/2, (self.world.min_y + self.world.max_y)/2)

        self.entities = set(filter(lambda x: self.is_inside(x.position), self.entities))

        #SHOOT    
        if len(self.players) > 1:
            nearest = None
            nearest_distance = None

            for player in self.players.values():
                if player != self.myself:
                    curr_distance = self.myself.position.distance(player.position)

                    if nearest is None or curr_distance < nearest_distance:
                        nearest = player.position
                        nearest_distance = curr_distance

            shoot = OneBulletShoot(self.myself.position.angle_to(nearest))

            if self.upgrades < 10:
                dx = (nearest.x - self.myself.position.x) * -20
                dy = (nearest.y - self.myself.position.y) * -20
                move = XY(dx, dy)
            else:
                if nearest_distance > 70:
                    move = self.towards(nearest) / 3 * 2

        elif len(self.entities) > 0:

            x_avg = sum([x.position.x for x in self.entities])/len(self.entities)
            y_avg = sum([x.position.y for x in self.entities])/len(self.entities)
            cluster = XY(x_avg, y_avg)


            nearest = None
            nearest_distance = None
        
            nearest_c = None
            nearest_c_distance = None
            
            for entity in self.entities:
                curr_c_distance = cluster.distance(entity.position)
                curr_distance = self.myself.position.distance(entity.position)

                if nearest_c is None or curr_c_distance < nearest_c_distance:
                    nearest_c = entity.position
                    nearest_c_distance = curr_c_distance

                if nearest is None or curr_distance < nearest_distance:
                    nearest = entity.position
                    nearest_distance = curr_distance

            shoot = OneBulletShoot(self.myself.position.angle_to(nearest))
            
            if self.last_pos is not None and (self.last_pos.distance(self.myself.position) < 15):
                if self.myself.position.distance(nearest_c) >= 50:
                    move = self.towards(nearest_c)
                else:
                    move = XY(0.001, 0)
            else:
                move = self.towards(cluster)

        
        boost = (shoot == NoShoot())
        
        # Check if we're outside the world area (or close to being outside)
        outside = False

        if self.world.min_x + self.EDGE_PADDING >= self.myself.position.x:
            move.x = 1000
            outside = True
        elif self.myself.position.x >= self.world.max_x - self.EDGE_PADDING:
            move.x = -1000
            outside = True 
        
        if self.world.min_y + self.EDGE_PADDING >= self.myself.position.y:
            move.y = 1000
            outside = True
        elif self.myself.position.y >= self.world.max_y - self.EDGE_PADDING:
            move.y = -1000
            outside = True

        # Prioritise getting back into arena over shooting someone/something
        boost |= outside
            
        if not outside and move == XY(0, 0):
            #MOVE
            bullets_others = {x for x in self.bullets if x.shooter_id != self._myself}

            s1 = Segment(self.myself.position, move)
            def check_collision(bullet: Bullet) -> bool:
                s2 = Segment(bullet.position, bullet.velocity)
                return Segment.collides(s1, self.myself.radius, s2, bullet.radius)
            
            colliding_bullets = set(filter(check_collision, bullets_others))

            if len(colliding_bullets) > 0:
                pass
            
            if self.next_target is None or self.myself.position.distance(self.next_target) < 75 \
                                        or not self.is_inside(self.next_target):
                self.next_target = self.random_position(center)
            move = self.towards(self.next_target)


        
        if self.myself.tank_updates_left > 0:
            new_tank = self.do_tank_update()
        
        if self.myself.levels_left > 0:
            stat = self.do_upgrade()
        

        if boost:
            dx = (move.x - self.myself.position.x) * -1
            dy = (move.y - self.myself.position.y) * -1
            shoot_c = XY(dx + self.myself.position.x, dy + self.myself.position.y)
            shoot = OneBulletShoot(self.myself.position.angle_to(shoot_c))

        self.last_pos = self.myself.position
        return Turn(move, shoot, stat, new_tank)



if __name__ == "__main__":
    p = Hrac()
    p.run()
