#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

class LepsiPlayer(ProbojPlayer):
    last_target = XY(inf, inf)
    last_direction = XY(inf, inf)
    last_position = XY(inf, inf)
    shooting_position = XY(inf, inf)
    next_upgrade = 0
    # TODO: add upgrades priorities
    upgrades = [StatsEnum.StatBulletTTL, StatsEnum.StatSpeed, StatsEnum.StatHealthMax]
    entities_map = {}
    turn = 0

    def in_map(self, position: XY) -> bool:
        return position.x < self.world.max_x and position.x > self.world.min_x and position.y < self.world.max_y and position.y > self.world.min_y
    
    def in_map_margin(self, position: XY) -> bool:
        return position.x < self.world.max_x * .9 and position.x > self.world.min_x * .9 and position.y < self.world.max_y * .9 and position.y > self.world.min_y * .9

    def closest_corner(self):
        my_position = self.myself.position
        closest_corner = XY(0.9*self.world.max_x, 0.9*self.world.max_y)
        if (my_position.distance(XY(0.9*self.world.max_x, 0.9*self.world.min_y)) < my_position.distance(closest_corner)):
            closest_corner = XY(0.9*self.world.max_x, 0.9*self.world.min_y)
        if my_position.distance(XY(0.9*self.world.min_x, 0.9*self.world.max_y)) < my_position.distance(closest_corner):
            closest_corner = XY(0.9*self.world.min_x, 0.9*self.world.max_y)
        if my_position.distance(XY(0.9*self.world.min_x, 0.9*self.world.min_y)) < my_position.distance(closest_corner):
            closest_corner = XY(0.9*self.world.min_x, 0.9*self.world.min_y)
        return closest_corner

    def shoot_entity(self) -> Shoot:
        self.log("lives left", self.myself.lifes_left)
        nearest = XY(inf, inf)
        nearest_player = False
        has_target = False
        num_entities = 0
        for entity in self.entities:
            if not self.in_map(entity.position):
                continue
            # TODO: do not shot if the bullet ttl and velocity would not get to the target
            num_entities += 1
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                nearest = entity.position
                self.shooting_position = self.myself.position
            if entity.position == self.last_target:
                nearest = self.last_target
                has_target = True
                break
        if not has_target:
            self.last_target = nearest # XY(inf,inf)
            self.shooting_position = self.myself.position # XY(inf, inf)
        else:
            self.last_target = nearest
            self.shooting_position = self.myself.position
        if num_entities == 0:
            max_health = inf
            for enemy in self.players.values():
                if enemy.health < max_health:
                    nearest = enemy.position
                    nearest_player = enemy
                    max_health = enemy.health
        # if self.myself.position == self.last_target:
        # self.log('has_target: ', has_target)
        # self.log('last_target:', self.last_target)
        # self.log('nearest', nearest)

        if self.myself.tank.tank_id == GuidedBulletTank.tank_id:
            self.log('Shooting guided missile')
            if nearest_player and nearest_player.position == nearest:
                return PlayerShoot(nearest_player.id)
            else:
                return XyShoot(nearest)
        else:
            return OneBulletShoot(self.myself.position.angle_to(nearest))

    def move(self):
        # TODO: if out of map, or going out of map, priority is to go to the center map
        next_direction = self.last_direction
        if next_direction.x == inf or next_direction.y == inf or not self.in_map_margin(next_direction):
            next_direction = XY(random.randint(int(self.world.min_x), int(self.world.max_x))* 0.8, 
                                random.randint(int(self.world.min_y), int(self.world.max_y))*0.8)
            self.last_direction = next_direction

        if self.last_target.x != inf and self.last_target.y != inf:
        #     self.log(self.last_target)
            next_direction = self.last_target
            my_pos = self.myself.position
            if (self.myself.position.distance(next_direction) < 25*self.myself.radius):
                next_direction = XY(-next_direction.x, -next_direction.y)
        if (self.world.max_x - self.world.min_x < 1000):
            next_direction = self.closest_corner()
        for bullet in self.bullets:
            # if bullet is originated from us, do not do anything
            if bullet.shooter_id == self.myself.id:
                continue
            s1 = Segment(bullet.position, bullet.position + bullet.velocity)
            s2 = Segment(self.myself.position, self.myself.position + next_direction)
            if Segment.collides(s1, bullet.radius, s2, self.myself.radius):
                next_direction *= -0.4

        # self.log(next_direction)
        return next_direction - self.myself.position

    def make_turn(self) -> Turn:
        self.log(f'Turn: {self.turn}')
        update_to = BasicTank.tank_id

        if len(self.myself.tank.updatable_to) != 0:
            self.log(self.myself.tank.updatable_to, TwinTank in self.myself.tank.updatable_to)
            if SniperTank in self.myself.tank.updatable_to:
                # if self.myself.stat_values[StatsEnum.StatBulletTTL] > 3:
                update_to = SniperTank.tank_id
            elif GuidedBulletTank in self.myself.tank.updatable_to:
                update_to = GuidedBulletTank.tank_id
            else:
                update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0
        next_stat = StatsEnum.StatNone
        if self.myself.levels_left > 0:
            next_stat = self.upgrades[self.next_upgrade]
            self.next_upgrade = (self.next_upgrade + 1)%(len(self.upgrades))

        return Turn(shoot=self.shoot_entity(),
                    velocity=self.move(),
                    stat= next_stat,
                    new_tank_id=update_to)

if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
