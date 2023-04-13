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
    upgrades = [StatsEnum.StatBulletSpeed, StatsEnum.StatHealthRegeneration, 
                StatsEnum.StatBulletDamage, StatsEnum.StatRange, StatsEnum.StatBulletTTL, StatsEnum.StatSpeed, 
                StatsEnum.StatReloadSpeed, StatsEnum.StatHealthMax]
    entities_map = {}
    turn = 0

    def in_map(self, position: XY) -> bool:
        return position.x < self.world.max_x and position.x > self.world.min_x and position.y < self.world.max_y and position.y > self.world.min_y
    def in_map_margin(self, position: XY) -> bool:
        return position.x < self.world.max_x * .9 and position.x > self.world.min_x * .9 and position.y < self.world.max_y * .9 and position.y > self.world.min_y * .9

    def shoot_entity(self):
        self.log("lives left", self.myself.lifes_left)
        nearest = XY(inf, inf)
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
                    max_health = enemy.health
        # if self.myself.position == self.last_target:
        self.log('has_target: ', has_target)
        self.log('last_target:', self.last_target)
        self.log('nearest', nearest)
        return nearest

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


        for bullet in self.bullets:
            # if bullet is originated from us, do not do anything
            if bullet.shooter_id == self.myself.id:
                continue
            s1 = Segment(bullet.position, bullet.position + bullet.velocity)
            s2 = Segment(self.myself.position, self.myself.position + next_direction)
            #if (Segment.collides(bullet, bullet.radius, next_direction, self.myself.radius)):
            if Segment.collides(s1, bullet.radius, s2, self.myself.radius):
                next_direction *= -0.4

        # self.log(next_direction)
        return next_direction - self.myself.position

    # filters out old, unupdated entites, which are in our range
    # def filter_old_entities(self):
    #     for entity in self.entities_map:
    #         e = self.entities_map[entity]

    #         # if entity is in our range, but was not updated, it is not here anymore
    #         if self.myself.position.distance(e['entity'].position) <= self.myself.stat_levels[StatsEnum.StatRange] and e['last_update'] < self.turn:
    #             # self.log(f'')
    #             del self.entities_map[entity]

    def make_turn(self) -> Turn:
        self.log(f'Turn: {self.turn}')
        nearest = XY(inf, inf)

        # for entity in self.entities:
        #     self.entities_map[entity.position] = {'entity': entity, 'last_update': self.turn}

        #     if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
        #         nearest = entity.position

        # self.filter_old_entities()

        # filter out removed entities

        # for player in self.players.values():
        #     if player != self.myself:
        #         self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
        #         if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
        #             nearest = player.position

        # for bullet in self.bullets:
        #     self.bullets_map[bullet.]

        # self.log("ideme na", nearest.x, nearest.y)

        if nearest == XY(inf, inf):
            nearest = XY(0, 0)

        update_to = BasicTank.tank_id

        if len(self.myself.tank.updatable_to) != 0:
            self.log(self.myself.tank.updatable_to, TwinTank in self.myself.tank.updatable_to)
            if SniperTank in self.myself.tank.updatable_to:
                if self.myself.stat_values[StatsEnum.StatBulletTTL] > 3:
                    update_to = SniperTank.tank_id
            elif MachineGunTank in self.myself.tank.updatable_to:
                update_to = MachineGunTank.tank_id
            else:
                update_to = random.choice([tank.tank_id for tank in self.myself.tank.updatable_to])
        else:
            update_to = 0
        next_stat = StatsEnum.StatNone
        if self.myself.levels_left > 0:
            next_stat = self.upgrades[self.next_upgrade]
            self.next_upgrade = (self.next_upgrade + 1)%(len(self.upgrades))

        self.turn += 1

        shoot = OneBulletShoot(self.myself.position.angle_to(self.shoot_entity()))

        # if self.myself.tank.tank_id == TwinTank.tank_id:
        #     self.log('shooting entity: ', self.shoot_entity())

        # self.log(self.myself.tank)

        # if self.myself.tank.tank_id == TwinTank.tank_id:
            # self.log('Twin tank, using two bullet shoot')
            # shoot = TwoBulletShoot(self.myself.position.angle_to(self.shoot_entity()), self.myself.position.angle_to(self.shoot_entity()))

        return Turn(shoot=shoot,
                    velocity=self.move(),
                    stat= next_stat,
                    new_tank_id=update_to)

if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
