#!/usr/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class MyPlayer(ProbojPlayer):
    def isOutOfBounds(self, entity):
        if entity.position.x <= self.world.min_x or entity.position.x >= self.world.max_x or entity.position.y <= self.world.min_y or entity.position.y >= self.world.max_y:
            return True
        return False
    def isInRange(self, entity, stats):
        # don't ask why, i have no fuckin idea
        if self.myself.position.distance(entity.position) <= stats[StatsEnum.StatBulletTTL] * stats[StatsEnum.StatBulletSpeed]:
            return True
        return False
    
    def isAlmostOutOfBounds(self, entity):
        if entity.position.x <= self.world.min_x + 50 or entity.position.x >= self.world.max_x - 50 or entity.position.y <= self.world.min_y + 50 or entity.position.y >= self.world.max_y -50:
            return True
        return False


    def make_turn(self) -> Turn:
        pos = XY(inf, inf)
        nearestEntity = None
        nearestPlayer = None
        stats = self.myself.stat_values
        shoot = NoShoot()

        for entity in self.entities:
            if not self.isOutOfBounds(entity) and (nearestEntity == None or self.myself.position.distance(entity.position) < self.myself.position.distance(nearestEntity.position)):
                nearestEntity = entity
    
        # if nearestEntity != None:
        #     dis = self.myself.position.distance(nearestEntity.position)
        #     shots = nearestEntity.health / stats[StatsEnum.StatBulletDamage]
        #     shootTime = shots * stats[StatsEnum.StatBulletTTL]
        #     walkTime = dis * stats[StatsEnum.StatSpeed]
        #     if shootTime < walkTime:
        #         pos = self.myself.position

        if nearestEntity:
            self.log(self.myself.position.distance(nearestEntity.position))
            if self.myself.tank.tank_id == 10:
                pos = self.myself.position
                shoot = OneBulletShoot(self.myself.position.angle_to(nearestEntity.position))
            # don't ask why, i have no fuckin idea
            elif self.isInRange(nearestEntity, stats):
                pos = self.myself.position
                shoot = OneBulletShoot(self.myself.position.angle_to(nearestEntity.position))
            else:
                pos = nearestEntity.position
        
        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                # we prioritize closest opponent!
                # and player.health != None and player.health < (float('inf') if nearestPlayer == None else nearestPlayer.health )
                if self.myself.tank.tank_id == 10 and not self.isOutOfBounds(player) and self.myself.position.distance(player.position) < (self.myself.position.distance(nearestPlayer.position) if nearestPlayer != None else float('inf')):
                    nearestPlayer = player
                    pos = player.position
                    shoot = OneBulletShoot(self.myself.position.angle_to(player.position))
                elif not self.isOutOfBounds(player) and self.isInRange(player, stats) and self.myself.position.distance(player.position) < (self.myself.position.distance(nearestPlayer.position) if nearestPlayer != None else float('inf')):
                    self.log(pos, shoot, "shoot player with health ", player.health, "instead of ", (float('inf') if nearestPlayer == None else nearestPlayer.health ))
                    nearestPlayer = player
                    # may need to go to the player aswell
                    pos = XY(self.myself.position.x, -self.myself.position.y)
                    shoot = OneBulletShoot(self.myself.position.angle_to(player.position))
                    #TODO tweak this
                elif not self.isOutOfBounds(player) and self.myself.position.distance(player.position) < (self.myself.position.distance(nearestPlayer.position) if nearestPlayer != None else float('inf')):
                    nearestPlayer = player
                    pos = player.position
        
        nearestBullet = None
        for bullet in self.bullets:
            seg = Segment(bullet.position, bullet.velocity)
            if Segment.segment_point_distance(seg, self.myself.position) <= self.myself.radius + bullet.radius:
                if float('inf') if nearestBullet == None else self.myself.position.distance(nearestBullet.position) > self.myself.position.distance(bullet.position):
                    nearestBullet = bullet
        
        if nearestBullet != None:
            pos = XY(nearestBullet.position.y, -nearestBullet.position.x)
            self.log("sidestepping from a bullet ", nearestBullet.position)
        
        if pos.x == inf or pos.y == inf:
            # pos = XY(random.randint(self.world.min_x + 1, self.world.max_x - 1), random.randint(self.world.min_y + 1, self.world.max_y - 1))
            pos = XY(0, 0)
        
        self.log("chod na: ",pos.x, pos.y)
        tanks = set([9, 10])
        update_to = 0

        if len(self.myself.tank.updatable_to) != 0:
            for tank in self.myself.tank.updatable_to:
                self.log(tank, tank.tank_id)
                if tank.tank_id in tanks:
                    update_to = tank.tank_id
                    break
        else:
            update_to = self.myself.tank.tank_id

        return Turn(velocity=pos - self.myself.position,
            shoot=shoot,
            stat=StatsEnum.StatSpeed,
            # stat=random.choice([StatsEnum.StatBodyDamage, StatsEnum.StatBulletDamage, StatsEnum.StatBulletSpeed, StatsEnum.StatBulletTTL, StatsEnum.StatHealthMax, StatsEnum.StatHealthRegeneration, StatsEnum.StatRange, StatsEnum.StatReloadSpeed, StatsEnum.StatSpeed]),
            new_tank_id=update_to)


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
                    stat=StatsEnum.StatHealthMax,
                    new_tank_id=update_to)


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
