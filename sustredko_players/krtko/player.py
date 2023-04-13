#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

def tank_rank(tank : Tank):
    if tank == BasicTank:
        return 1
    elif tank == TwinTank or tank == SniperTank or tank == AsymetricTank:
        return 3
    else:
        return 9


class LepsiPlayer(ProbojPlayer):
    def find_sorted_entities(self)->Entity:
        "Sortene entity podla najblizsej"
        return sorted(self.entities, key = lambda x : self.myself.position.distance(x.position))
    
    def edge_world_pos(self)->XY:
        "Kam sa pohnut aby som isiel na kraj"
        r = self.myself.radius
        self.log(self.world.max_x, self.world.max_y)
        return XY(self.world.max_x - r, self.world.max_y - r) - self.myself.position
    def precomp(self):
        """Predpocita nejake usefull veci. Zatial iba zoradzuje playerov,
        bullets a entities."""
        self.sorted_bullets = self.sort_by_dist(self.bullets)
        self.sorted_players = self.sort_by_dist(self.players_without_me())
        self.sorted_entities = self.sort_by_dist(self.entities)

    def players_without_me(self) -> list[Player]:
        """Vrati list s playermi bez nas."""
        return [player for player in self.players.values()
            if player != self.myself]

    def sort_by_dist(self, iterable) -> list[any]:
        """Zoradi danu iterable podla vzdialenosti od nasho tanku
        a vrati list s prvkami zoradenymi vzostupne. Iterable musi
        obsahovat objekty s poziciou (.position)."""
        l = [x for x in iterable]
        return sorted(l, key = lambda \
            x : self.myself.position.distance(x.position))
    
    def is_closest_player_stronger(self)->bool:
        """Vrati ci je najblizsi tank silnejsi ako ja"""

    def dodge_strongest_bullet(self) -> XY:
        """Vrati vektor, ktorym ak sa pohneme, vyhneme sa bullet s max.
        damagom, ktora do nas v najblizsom tiku zrazi. Ak taka bullet
        neexistuje, vrati vektor XY(inf, inf)."""
        bullets_to_hit = [bullet for bullet in self.sorted_bullets
            if self.is_going_to_hit_me(bullet)]
        bullets_to_hit.sort(key = lambda x : x.damage)
        if not bullets_to_hit:
            return XY(inf, inf)
        most_dangerous = bullets_to_hit[-1]
        # vrati normalovy (kolmy) vektor na vektor smeru najblizsej bullet
        return XY(-most_dangerous.position.y, most_dangerous.position.x)

    def is_going_to_hit_me(self, bullet) -> bool:
        """Vrati True ak do nas nejaka bullet v najblizsom tiku narazi."""
        seg = Segment(bullet.position, bullet.velocity)
        if seg.segment_point_distance(seg,
            self.myself.position) <= bullet.radius + self.myself.radius:
            return True
        return False

    def per_quads(self, iterable) -> list[tuple]:
        """Priradi rovnake cisla objektom v ronakom kvadrane."""
        l = []
        for x in iterable:
            if x.position.x < self.world.min_x: continue
            if x.position.x > self.world.max_x: continue
            if x.position.y < self.world.min_y: continue
            if x.position.y > self.world.max_y: continue

            if x.position.x >= self.myself.position.x and \
                x.position.y >= self.myself.position.y:
                l.append((x, 0))
            if x.position.x < self.myself.position.x and \
                x.position.y >= self.myself.position.y:
                l.append((x, 1))
            if x.position.x < self.myself.position.x and \
                x.position.y < self.myself.position.y:
                l.append((x, 2))
            else:
                l.append((x, 3))
        return l

    def best_quad(self):
        scores = [0 for _ in range(4)]

        for player, q in self.per_quads(self.players_without_me()):
            distance = self.myself.position.distance(player.position) 
            if distance == 0: continue
            rank = tank_rank(player.tank)
            index = (-1000 * rank) / math.sqrt(distance)
            scores[q] += index

        for bullet, q in self.per_quads(self.bullets):
            distance = self.myself.position.distance(bullet.position) 
            if distance == 0: continue
            damage = bullet.damage
            index = (- 100 * damage) / math.sqrt(distance)
            scores[q] += index
            
        for entity, q in self.per_quads(self.entities):
            distance = self.myself.position.distance(entity.position)
            if distance == 0: continue
            index = 1 / math.sqrt(distance)
            scores[q] += index

        for i in range(len(scores)):
            if scores[i] == max(scores):
                return i
        return 0

    def stat_to_update(self):
        stats = self.myself.stat_levels.stats
        a = StatsEnum
        st_res = [a.StatNone, a.StatRange,
            a.StatSpeed, a.StatBulletSpeed,
            a.StatBulletTTL, a.StatBulletDamage,
            a.StatHealthMax, a.StatHealthRegeneration,
            a.StatBodyDamage, a.StatReloadSpeed]

        prio = [2, 6, 7, 5, 4, 9, 3, 1]
        for x in prio:
            if stats[x] < 7:
                return st_res[x]
        return st_res[0]
            
    def make_turn(self) -> Turn:
        # predpocitame potrebne veci
        self.precomp()

        # nahodne vyberiem novy upgrade tanku ak mozeme
        av_tanks = [tank.tank_id for tank in self.myself.tank.updatable_to]
        if 5 in av_tanks:
            update_to = 5
        elif 8 in av_tanks:
            update_to = 7
        else:
            update_to = 0

        # vyberieme najblizsiu entitu, ak ziadne entity nevidime, povazujeme
        # nasu poziciu za entitu
        if self.sorted_entities:
            nearest_entity = self.sorted_entities[0]
        else:
            nearest_entity = Entity(self.myself.position, 0, 0)

        # vyhneme sa najsilnejsej bullet, ktora do nas ide narazit
        velocity = self.dodge_strongest_bullet()
        if self.sorted_entities:
            target = self.sorted_entities[0].position
        else:
            target = XY(inf, inf)

        if velocity.x != inf and velocity.y != inf:
            self.log("vyhybame sa najsilnejsej bullet, ideme smerom",
                velocity)
        else:
            # defaultne chceme ist do stredu akutalnej mapy
            mid = XY((self.world.max_x + self.world.min_x) / 2,
                (self.world.max_y + self.world.min_y) / 2)
            velocity = mid - self.myself.position
            if velocity.x == 0 and velocity.y == 0:
                velocity = XY(1000, 1000)
            
            # najdeme najlepsi kvadrant
            b = self.best_quad()
            entities = [e for e, q in self.per_quads(self.entities) if q == b]
            entities = self.sort_by_dist(entities)
            if entities:
                target = entities[0].position
                if self.myself.position.distance(target) < \
                    self.myself.radius + entities[0].radius + 50:
                    velocity = entities[0].position - self.myself.position
                    velocity.x *= -1000
                    velocity.y *= -1000
                    self.log("health ", entities[0].health)
                else:
                    velocity = entities[0].position - self.myself.position
            else:
                # if b == 0: velocity = XY(100, 100)
                # elif b == 1: velocity = XY(-100, 100)
                # elif b == 2: velocity = XY(-100, -100)
                # elif b == 3: velocity = XY(100, -100)
                if self.sorted_entities:
                    target = self.sorted_entities[0].position

        # self.log("target ", target)
        # self.log("velocity ", velocity)
        self.log("tank:", self.myself.tank.tank_id)
        self.log(self.myself.stat_levels.stats)
        if self.myself.tank.tank_id == 7 and self.sorted_players and \
            self.myself.position.distance(self.sorted_players[0].position) <= \
            self.myself.stat_values.stats[1] / 2:
            self.log("Shooting player")
            shoot = PlayerShoot(self.sorted_players[0].id)
        elif self.myself.tank.tank_id == 7:
            self.log("Shooting entity")
            shoot = XyShoot(target)
        else:
            self.log("Shooting entity")
            self.log("target ", target)
            shoot = OneBulletShoot(self.myself.position.angle_to(target))

        self.log(len(self.myself.stat_values.stats))
        return Turn(velocity=velocity,
                    shoot=shoot,
                    stat=self.stat_to_update(),
                    new_tank_id=update_to)
        
if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()


