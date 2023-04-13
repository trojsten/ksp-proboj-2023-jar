#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

SAFE_VZDIALENOST_OD_KRAJU = 250
class NajlepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        if self.lastHealth != self.myself.health:
            self.log('was hit')
            self.lastHealth = self.myself.health
        movement = XY(0,0)
        tank = self.najblizsi_tank()
        entita = self.najblizsia_entita()
        shoot = NoShoot()
        if tank is not None and self.path_clear(tank.position):
            self.log('tank')
            dist = XY.distance(self.myself.position, tank.position)
            if self.myself.reload_cooldown == 0 and dist < self.get_range:
                self.log('shoot tank')
                target = tank.position
                if tank.id in self.lastPositions:
                    tankVelocity = tank.position - self.lastPositions[tank.id]
                    tickToHit = dist / self.myself.stat_values[StatsEnum.StatBulletSpeed]
                    target += tankVelocity * tickToHit
                shoot = OneBulletShoot(self.myself.position.angle_to(target))
            movement = self.random_inside_circle(30, (tank.position - self.myself.position).normalize() * (dist - min(self.get_range, self.get_visibility)))
        elif entita is not None:
            self.log('entita')
            dist = XY.distance(self.myself.position, entita.position)
            self.log('distance od entity: {dist}' .format(dist = dist))
            self.log('dostrel: {range}, cooldown: {cooldown}' .format(range=self.get_range, cooldown = self.myself.reload_cooldown))
            # target = entita.position
            if self.myself.reload_cooldown == 0 and dist < self.get_range:
                self.log('shoot')
                shoot = OneBulletShoot(self.myself.position.angle_to(entita.position))
            movement = (entita.position - self.myself.position).normalize() * (dist - max(0.9 * self.get_range, 40))
            self.log('chcena vzdialenost od entity: {dist}' .format(dist = dist - max(0.9 * self.get_range, 40)))
        else:
            self.log('ku stredu')
            stred = XY((self.world.max_x + self.world.min_x)/2, (self.world.max_y + self.world.min_y)/2)
            radius = min(self.world.max_x-self.world.min_x, self.world.max_y-self.world.min_y)/4
            target = self.random_inside_circle(radius, stred)
            movement = target - self.myself.position
        if self.je_blizko_kraju():
            self.log('blizko kraju')
            stred = XY((self.world.max_x + self.world.min_x)/2, (self.world.max_y + self.world.min_y)/2)
            radius = min(self.world.max_x-self.world.min_x, self.world.max_y-self.world.min_y)/4
            target = self.random_inside_circle(radius, stred)
            movement = target - self.myself.position
        stat = StatsEnum.StatNone

        # if len(sys.argv) > 1 and sys.argv[1] == 'avoid':
        #     if self.je_v_ceste_naboj(target):
        #         self.log('Cakame, lebo je v ceste naboj')
        #         for _ in range(3):
        #             self.movequeue.insert(0, XY(0,0))

        if self.myself.levels_left > 0:
            stat = self.upgrade()
        
        naboje = self.zisti_ohrozujuce_naboje()
        if len(naboje) >= 1:
            self.log('avoiding ' + str(len(naboje)) + ' bullets')
            smer = XY(0,0)
            for naboj in naboje:
                self.log('bullet speed: {speed}'.format(speed=naboj.velocity))
                smer += XY(naboj.velocity.y, -naboj.velocity.x).normalize()
            self.log('final direction: {smer}'.format(smer = smer))
            if len(self.movequeue) > 0 and self.movequeue[0] != smer:
                self.movequeue.clear()
            for _ in range(5):
                self.movequeue.append(smer*1000)
        
        if len(self.movequeue) > 0:
            movement = self.movequeue.pop(0)
        self.update_velocities()
        return Turn(movement,
                    shoot,
                    stat=stat,
                    new_tank_id=self.tank_strategy().tank_id)
    
    def je_blizko_kraju(self):
        pozicia = self.myself.position
        svet = self.world
        return pozicia.x - svet.min_x < SAFE_VZDIALENOST_OD_KRAJU or svet.max_x - pozicia.x < SAFE_VZDIALENOST_OD_KRAJU or pozicia.y - svet.min_y < SAFE_VZDIALENOST_OD_KRAJU or svet.max_y - pozicia.y < SAFE_VZDIALENOST_OD_KRAJU

    def update_velocities(self):
        self.lastPositions.clear()
        for tank in self.players.values():
            self.lastPositions[tank.id] = tank.position

    def zisti_ohrozujuce_naboje(self) -> List["Bullet"]:
        ret = []
        for bullet in self.bullets:
            usecka = Segment(bullet.position, bullet.velocity)
            if Segment.segment_point_distance(usecka, self.myself.position) < bullet.radius + self.myself.radius:
                ret.append(bullet)
        return ret
    
    def je_v_ceste_naboj(self, target: "XY") -> bool:
        s1 = Segment(self.myself.position, target)
        ticks = XY.distance(target, self.myself.position) / self.get_speed + 1
        for bullet in self.bullets:
            if bullet.shooter_id == self.myself.id:
                continue
            self.log(bullet.velocity * ticks)
            s2 = Segment(bullet.position, bullet.position + (bullet.velocity * ticks))
            intersection = Segment.get_segment_intersection(s1,s2)
            if intersection is not None:
                ticksPlayer = XY.distance(self.myself.position, intersection) / self.get_speed
                ticksBullet = XY.distance(bullet.position, intersection) / bullet.velocity.length()
                if abs(ticksBullet - ticksPlayer) < 2:
                    return True
                
        return False
            

    def najblizsia_entita(self):
        ret = None
        dist = inf
        for entity in self.entities:
            x = entity.position.x
            y = entity.position.y
            if x + SAFE_VZDIALENOST_OD_KRAJU > self.world.max_x or x - SAFE_VZDIALENOST_OD_KRAJU < self.world.min_x or y + SAFE_VZDIALENOST_OD_KRAJU > self.world.max_y or y - SAFE_VZDIALENOST_OD_KRAJU < self.world.min_y:
                continue
            if XY.distance(self.myself.position, entity.position) < dist:
                dist = XY.distance(self.myself.position, entity.position)
                ret = entity
        return ret
    
    def najblizsi_tank(self) -> "Player":
        ret = None
        dist = inf
        for entity in self.players.values():
            if entity.id == self._myself:
                continue
            if XY.distance(self.myself.position, entity.position) < dist:
                dist = XY.distance(self.myself.position, entity.position)
                ret = entity
        return ret
    
    def time_before_hit(self, bullet: "Bullet"):
        distance = XY.distance(self.myself.position, bullet.position)
        velocity = math.sqrt(bullet.velocity.x ** 2 + bullet.velocity.y ** 2)
        return distance / velocity


    def random_inside_circle(self, r: int, pos: "XY") -> "XY": 
        a = random.random() * r
        angle = random.random() * 2 * math.pi
        return pos + XY(a* math.cos(angle), math.sin(angle))
    
    @property
    def get_range(self) -> float:
        r = self.myself.stat_values[StatsEnum.StatBulletTTL] * self.myself.stat_values[StatsEnum.StatBulletSpeed]
        if r > 0:
            self.range = r
        else:
            r = self.range

        return r
    
    @property
    def get_speed(self) -> float:
        return self.myself.stat_values[StatsEnum.StatSpeed]

    @property
    def get_visibility(self) -> float:
        return self.myself.stat_values[StatsEnum.StatRange]

    def upgrade(self) -> "StatsEnum":
        upgrady = sum(self.myself.stat_levels.stats)
        weights = {
            StatsEnum.StatBulletDamage: 6,
            StatsEnum.StatBulletSpeed: 5,
            StatsEnum.StatReloadSpeed: 7,
            StatsEnum.StatBulletTTL: 1,
            StatsEnum.StatSpeed: 6,
            StatsEnum.StatRange: 2
        }
        s = []
        for i in weights.keys():
            for j in range(weights[i]):
                s.append(i)
        stat = random.choice(s)
        while self.myself.stat_levels[stat] == 7:
            stat = random.choice(s)
        if upgrady < 6:
            if self.myself.stat_levels[StatsEnum.StatSpeed] >= 2:
                stat = StatsEnum.StatReloadSpeed
            elif self.myself.stat_levels[StatsEnum.StatReloadSpeed] >= 2:
                stat = StatsEnum.StatSpeed
            else:
                stat = random.choice([StatsEnum.StatSpeed, StatsEnum.StatReloadSpeed])
        if upgrady == 0:
            stat = StatsEnum.StatBulletTTL
        return stat

    def tank_strategy(self) -> "Tank":
        if self.myself.tank_updates_left > 0:
            if self.myself.tank == BasicTank():
                return SniperTank()
            elif self.myself.tank == TwinTank():
                return DoubleDoubleTank()
        return self.myself.tank                


    def path_clear(self, target: XY) -> "bool":
        s = Segment(self.myself.position, target)
        for entity in self.entities:
            if Segment.segment_point_distance(s, entity.position) < entity.radius + self.myself.radius:
                return False
        return True


    def __init__(self):
        self.movequeue: list["XY"] = []
        self.lastPositions: dict[int:"XY"] = {}
        self.lastHealth: float = -1
        super().__init__()