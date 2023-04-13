#!/bin/env python3
import math
import random
import time
from math import inf

from constants import upgrades
from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
from libs.stats import StatsEnum


# Calculates where to shoot to hit the target
def shooting(self, go_to):
    shoot_at = XY(inf, inf)

    entity = False
    play_id = 0
    for entity in self.entities:
        if self.myself.position.distance(entity.position) < self.myself.position.distance(shoot_at):
            # shoot_at = XyShoot(entity.position - self.myself.position)

            shoot_at = entity.position
            entity = True

    for player in self.players.values():
        if player != self.myself:
            if self.myself.position.distance(player.position) < self.myself.position.distance(shoot_at):
                shoot_at = player.position
                entity = False
                play_id = player.id

    if shoot_at == XY(inf, inf):
        shoot_at = - (go_to - self.myself.position)

    # if entity:
    #     shoot_final = XyShoot(shoot_at)
    # else:
    #     shoot_final = PlayerShoot(play_id)
    shoot_final = OneBulletShoot(self.myself.position.angle_to(shoot_at))

    # if shoot_at == XY(inf, inf):
    #     shoot_at = - (go_to - self.myself.position)
    return shoot_final


# Calculate where to go, not to go inside a target
def calculate_nearest_point(target, target_distance: int, radius, tank, player, self):
    if target_distance < radius + player.radius + 50 and tank.tank_id != 10 and self.myself.health > 30:
        return player.position
    else:
        return target


# Check if the desired destination is valid
def off_world_and_inf_checking(nearest, self):
    if nearest.x < self.world.min_x or nearest.x > self.world.max_x:
        nearest.x = - nearest.x
    if nearest.y < self.world.min_y or nearest.y > self.world.max_y:
        nearest.y = - nearest.y
    if nearest.x == inf or nearest.y == inf or nearest.x == -inf or nearest.y == -inf or self.myself.health < 30:
        nearest = XY((self.world.max_x + self.world.min_x) / 2, (self.world.max_y + self.world.min_y) / 2)

    return nearest


# Determines how to upgrade the tank
def tank_updating(self):
    update_to = 0
    my_id = self.myself.tank.tank_id

    if len(self.myself.tank.updatable_to) != 0:
        if my_id == 0:
            update_to = 9
        elif my_id == 9:
            update_to = 10

    return update_to


# Logging function
def log(player: ProbojPlayer, message):
    player.log(
        f'<{player.myself.level}> [{player.myself.tank}] [{player.myself.health} HP] {player.myself.position}, ' +
        f'stats [{player.myself.stat_levels[StatsEnum.StatRange]}, ' +
        f'{player.myself.stat_levels[StatsEnum.StatSpeed]}, ' +
        f'{player.myself.stat_values[StatsEnum.StatBulletSpeed]}, ' +
        f'{player.myself.stat_values[StatsEnum.StatBulletTTL]}, ' +
        f'{player.myself.stat_levels[StatsEnum.StatHealthMax]}, ' +
        f'{player.myself.stat_levels[StatsEnum.StatHealthRegeneration]}, ' +
        f'{player.myself.stat_levels[StatsEnum.StatBodyDamage]}, ' +
        f'{player.myself.stat_levels[StatsEnum.StatReloadSpeed]}]: {message}')


ticks = 0


# Determines where to go
def where_to_initially(self):
    # Determine which entity is nearest
    nearest_entity = XY(inf, inf)
    for entity in self.entities:
        if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest_entity):
            nearest_entity = calculate_nearest_point(entity.position,
                                                     self.myself.position.distance(entity.position),
                                                     entity.radius,
                                                     self.myself.tank, self.myself, self)

    # Determines which player is nearest
    nearest_player = XY(inf, inf)
    for player in self.players.values():
        if player != self.myself:
            if self.myself.position.distance(player.position) < self.myself.position.distance(nearest_player):
                nearest_player = player.position

    # Determines whether the bot should follow an entity or a player
    nearest = XY(inf, inf)
    if self.myself.level > 20 and nearest_player.x != inf and nearest_player.y != inf and self.myself.health > 30:
        nearest = nearest_player
    elif nearest_entity.x != inf and nearest_entity.y != inf:
        nearest = nearest_entity
    elif nearest_player.x != inf and nearest_player.y != inf and self.myself.health > 50:
        nearest = nearest_player
    else:
        # Goes to middle if there are no interesting targets
        nearest = XY((self.world.max_x + self.world.min_x) / 2, (self.world.max_y + self.world.min_y) / 2)

    return nearest

def shoot_avoiding(self: ProbojPlayer, nearest):
    dot_product = nearest

    # return dot_product
    for incoming_shot in self.bullets:

        normal_vel = XY(-incoming_shot.velocity.y, incoming_shot.velocity.x)
        c = -(normal_vel.x * incoming_shot.position.x +
              normal_vel.y * incoming_shot.position.y)

        x, y = self.myself.position.x, self.myself.position.y
        bx, by = incoming_shot.position.x, incoming_shot.position.y
        in_way = normal_vel.x * x + normal_vel.y * y + c

        # self.log(f'incoming shot - ona {bx, by} a ja {x, y}')
        distance = math.sqrt((x - bx) ** 2 + (y - by) ** 2)
        if math.sqrt(incoming_shot.velocity.x ** 2
                     + incoming_shot.velocity.y ** 2) * incoming_shot.ttl \
                > distance and abs(in_way) + self.myself.radius < 50:
            dot_product = ((dot_product - self.myself.position) + normal_vel) + self.myself.position

    return dot_product


class LepsiPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        # Keeps track of ticks
        global ticks
        ticks += 1

        '''
        * Determine where to go
        '''
        nearest = where_to_initially(self)

        '''
        * Check if it is valid
        '''
        nearest = off_world_and_inf_checking(nearest, self)
        # XY((self.world.max_x + self.world.min_x) / 2, (self.world.max_y + self.world.min_y) / 2)
        if nearest.x == (self.world.max_x + self.world.min_x) / 2 and nearest.y == (self.world.max_y + self.world.min_y) / 2 \
            and self.myself.position.distance(XY((self.world.max_x + self.world.min_x) / 2, (self.world.max_y + self.world.min_y) / 2)) < 200:
            nearest = XY(self.world.max_x - 10, self.world.max_y - 10) + self.myself.position

        '''
        * Upgrade the tank
        '''
        update_to = tank_updating(self)

        '''
        * Shoot
        '''
        shoot = shooting(self, nearest)

        '''
        * Shoot avoiding
        '''
        nearest = shoot_avoiding(self, nearest)
        # Submits the next turn

        # self.log(self.myself.radius)
        # todo stojime v strede sveta a nehybeme sa
        return Turn(velocity=nearest - self.myself.position,
                    shoot=shoot,
                    stat=upgrades[self.myself.level - 1],
                    new_tank_id=update_to)


# ! 1. strielanie na entity a tanky
# ! 2. posuvanie
# ! 3. uptadeovat tank
# ! 4. uhybanie strelam

if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
