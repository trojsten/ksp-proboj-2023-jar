import random
from math import inf
import math

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


def in_shooting_range(self: ProbojPlayer, target: XY) -> bool:
    dist = self.myself.position.distance(target)
    srange = (
        self.myself.stat_values[StatsEnum.StatBulletTTL]
        * self.myself.stat_values[StatsEnum.StatBulletSpeed]
    )
    return dist < srange


def old_find_target(self: ProbojPlayer):
    for player in self.players.values():
        if player == self.myself:
            continue
        if in_shooting_range(self, player.position):
            return OneBulletShoot(self.myself.position.angle_to(player.position))

    for entity in self.entities:
        if in_shooting_range(self, entity.position):
            return OneBulletShoot(self.myself.position.angle_to(entity.position))
    return NoShoot()


def shoot_nearest(self: ProbojPlayer):
    mam = False
    nearest = XY(inf, inf)
    go_for_player=False
    target_id=-1
    got_player=False
    if self.myself.tank.tank_id==7:
        go_for_player=True
    for player in self.players.values():
        if player == self.myself:
            continue
        if in_shooting_range(self, player.position):
            if self.myself.position.distance(player.position)<self.myself.position.distance(nearest):
                mam = True
                got_player=True
                nearest =player.position
                target_id=player.id
                
    want_entity=True
    if self.myself.position.distance(nearest)<self.myself.stat_values[StatsEnum.StatBulletSpeed]*2:
        want_entity=False    
    for entity in self.entities:
        if in_shooting_range(self, entity.position):
            if got_player and go_for_player:continue
            if want_entity or self.myself.position.distance(entity.position)<self.myself.position.distance(nearest):
                mam=True
                nearest =entity.position
                want_entity=False

    if go_for_player:
        if mam:
            if target_id!=-1: return PlayerShoot(target_id)
            else: return XyShoot(nearest)
        else: return NoShoot()

    if mam: return OneBulletShoot(self.myself.position.angle_to(nearest))
    return NoShoot()