#!/bin/env python3
import random
from math import inf, cos, pi, radians, nan

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
from libs.stats import *

class OurPlayer(ProbojPlayer):
    def __init__(self):
        self.last_on_mid = -10000
        self.tick = 0
        self.previous_id = None
        self.previous_position = XY(inf, inf)
        self.from_mid = XY(random.randint(-8000, 8000), random.randint(-8000, 8000))

    def make_turn(self) -> Turn:
        self.tick += 1

        x = self.myself.position.x
        y = self.myself.position.y
        nearest_entity = XY(inf, inf)
        nearest_player = XY(inf, inf)
        player_id = None

        direction = XY(inf, inf)

        ttl = self.myself.stat_values[StatsEnum.StatBulletTTL]
        speed = self.myself.stat_values[StatsEnum.StatBulletSpeed]
        bullet_distance = ttl * speed

        max_x, min_x = self.world.max_x, self.world.min_x
        max_y, min_y = self.world.max_y, self.world.min_y
        
        for entity in self.entities:
            if max_x > entity.position.x > min_x and max_y > entity.position.y > min_y:
                if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest_entity):
                    nearest_entity = entity.position
    
        for player in self.players.values():
            if player != self.myself:
                # self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_player):
                    player_id, nearest_player = player.id, player.position
        
        # Calculate where the player is going to be
        predicted = nearest_player
        if nearest_player.x != inf:
            self.log("Player:", nearest_player)
            self.log("Previous:", self.previous_position)
            v_e = nearest_player.distance(self.previous_position)
            d = self.myself.position.distance(nearest_player)
            if d*v_e != 0:
                cos_alpha = XY.dot(nearest_player - self.previous_position, self.myself.position - nearest_player) / (d * v_e)
                v_b = speed
                discriminant = 4 * v_e ** 2 * cos_alpha ** 2 + 4 * (v_b ** 2 - v_e ** 2) * d ** 2
                if discriminant > 0:
                    t = (-2 * v_e * d * cos_alpha + math.sqrt(4 * v_e ** 2 * cos_alpha ** 2 + 4 * (v_b ** 2 - v_e ** 2) * d ** 2)) / (2 * (v_b ** 2 - v_e ** 2))
                    self.log("Diskriminant:", discriminant)
                    self.log("v_b:", v_b)
                    self.log("v_e:", v_e)
                    self.log("t:", t)
                    predicted = nearest_player + XY((nearest_player.x - self.previous_position.x)*t, (nearest_player.y - self.previous_position.y)*t) 
                    self.log("Predicted player:", predicted)
        #self.log("ideme na", nearest.x, nearest.y)


        MAX_BORDER_DISTANCE = 300
        BULLET_DISTANCE_TOLLERANCE = 30
        NEAR_BORDER_THRESHOLD = 50
        MID_COOLDOWN = 50

        for bullet in self.bullets:
            if bullet.shooter_id != self.myself.id and self.myself.position.distance(bullet.position) > \
                self.myself.position.distance(bullet.position + bullet.velocity):
                x0, y0, x1, y1, x2, y2 = self.myself.position.x, self.myself.position.y, bullet.position.x, \
                    bullet.position.y, bullet.position.x + bullet.velocity.x, bullet.position.y + bullet.velocity.y
                line_point_distance = ((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / bullet.position.distance(bullet.position + bullet.velocity)
                if line_point_distance <= (bullet.radius + self.myself.radius)*2:
                    if bullet.velocity.x * (self.myself.position.y - bullet.position.y) - bullet.velocity.y * (self.myself.position.x - bullet.position.x) > 0:
                        direction = self.myself.position + XY(-1000 * bullet.velocity.y, 1000 * bullet.velocity.x)
                    else:
                        direction = self.myself.position + XY(1000 * bullet.velocity.y, -1000 * bullet.velocity.x)

        if direction.x == inf and direction.y == inf:

            # Low health retreat
            p1 = self.myself.health < 0.3*self.myself.stat_values[StatsEnum.StatHealthMax]
            p2 = nearest_player.x != inf
            p3 = x - min_x < NEAR_BORDER_THRESHOLD or max_x - x < NEAR_BORDER_THRESHOLD or y - min_y < NEAR_BORDER_THRESHOLD or max_y - y < NEAR_BORDER_THRESHOLD
            if p1 and p2 and p3:
                direction = XY(-nearest_player.x, -nearest_player.y)


            # Moving
            elif nearest_player.x != inf:
                if self.myself.position.distance(predicted) > bullet_distance - BULLET_DISTANCE_TOLLERANCE:
                    direction = predicted
                else:
                    direction = self.myself.position
            elif nearest_entity.x != inf:
                if self.myself.position.distance(nearest_entity) > bullet_distance  - BULLET_DISTANCE_TOLLERANCE:
                    direction = nearest_entity
                else: 
                    direction = self.myself.position
                #TODO rozumnejsie predpovedanie polohy nepriatela

            # Moving away from border
            elif x - min_x < MAX_BORDER_DISTANCE:
                self.last_on_mid = 0
                direction = XY(max_x, y)
            elif max_x - x < MAX_BORDER_DISTANCE:
                self.last_on_mid = 0
                direction = XY(min_x, y)
            elif y - min_y < MAX_BORDER_DISTANCE:
                self.last_on_mid = 0
                direction = XY(x, max_y)
            elif max_y - y < MAX_BORDER_DISTANCE:
                self.last_on_mid = 0
                direction = XY(x, min_y)
            
            
            # Move in random direction when on mid
            elif x == (min_x + max_x)/2 and y == (min_y + max_y)/2:
                self.last_on_mid = self.tick
                self.from_mid = XY(random.randint(-8000, 8000), random.randint(-8000, 8000))
                direction = self.from_mid

            # Move to mid
            elif self.tick - self.last_on_mid > MID_COOLDOWN:
                direction = XY((min_x + max_x)/2, (min_y + max_y)/2)

            else:
                direction = self.from_mid

            self.log("My Position:", x, y)
            self.log("ttl:", ttl)
            self.log("speed:", speed)


        # Shooting
        bullet_direction = None
        if nearest_player.x != inf and self.myself.position.distance(predicted) < bullet_distance:           
            bullet_direction = predicted
            
        elif self.myself.position.distance(nearest_entity) <= bullet_distance:
            bullet_direction = nearest_entity

        if bullet_direction is None:
            shoot = NoShoot()
        else:
            shoot = OneBulletShoot(self.myself.position.angle_to(bullet_direction))
            

        stat = 0       
        sum_ = 0
        for stat in StatsEnum:
            sum_ += self.myself.stat_levels[stat]

        stat_list = [StatsEnum.StatRange, StatsEnum.StatBulletDamage, StatsEnum.StatBulletTTL, StatsEnum.StatReloadSpeed, StatsEnum.StatSpeed]*2
        # stat_list += [StatsEnum.StatHealthMax, StatsEnum.StatHealthRegeneration]
        
        # stat_list = [StatsEnum.StatSpeed, StatsEnum.StatReloadSpeed, StatsEnum.StatBulletDamage, StatsEnum.StatBulletTTL]*10
        # stat_list = [StatsEnum.StatSpeed]*20

        stat_choices = list(StatsEnum)
        if sum_ < len(stat_list):
            stat = stat_list[sum_]
        else:
            stat = random.choice(stat_choices)

        tank1 = SniperTank
        tank2 = MachineGunTank

        
        # tank1 = AsymetricTank
        # tank2 = AsymetricTripleTank

        if tank1 in self.myself.tank.updatable_to:
            update_to = tank1.tank_id
        elif tank2 in self.myself.tank.updatable_to:
            update_to = tank2.tank_id
        else:
            update_to = 0


        #TODO strielanie na nepriatela mimo zorneho pola

        self.previous_id = player_id
        self.previous_position = nearest_player
        
        return Turn(velocity=direction - self.myself.position,
                    shoot=shoot,
                    stat=stat,
                    new_tank_id=update_to)
    


if __name__ == "__main__":
    p = OurPlayer()
    p.run()
