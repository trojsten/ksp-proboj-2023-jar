from math import inf
from typing import Union
from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


def nearest_entity(self: ProbojPlayer, limit: float = inf) -> Union[Entity, None]:
    nearest: Union[Entity, None] = None
    for entity in self.entities:
        if nearest is None:
            nearest = entity

        dist_entity = self.myself.position.distance(entity.position)
        dist_nearest = self.myself.position.distance(nearest.position)
        if dist_entity < dist_nearest:
            nearest = entity

    if nearest is not None and self.myself.position.distance(nearest.position) > limit:
        return None
    return nearest


def nearest_player(self: ProbojPlayer, limit: float = inf) -> Union[Player, None]:
    nearest: Union[Player, None] = None
    for player in self.players.values():
        if player == self.myself:
            continue
        if nearest is None:
            nearest = player

        dist_player = self.myself.position.distance(player.position)
        dist_nearest = self.myself.position.distance(nearest.position)
        if dist_player < dist_nearest:
            nearest = player

    if nearest is not None and self.myself.position.distance(nearest.position) > limit:
        return None
    return nearest


def my_shoot_range(self: ProbojPlayer) -> float:
    ttl = self.myself.stat_values[StatsEnum.StatBulletTTL]
    speed = self.myself.stat_values[StatsEnum.StatBulletSpeed]
    return ttl * speed


def threatening_bullet(self: ProbojPlayer) -> Union[Bullet, None]:
    pos = self.myself.position
    for b in self.bullets:
        if pos.distance(b.position) <= b.velocity.distance(XY(0, 0)) * b.ttl and bullet_intersects(b, self.myself):
            return b


def bullet_intersects(bullet: Bullet, player: Player) -> bool:
    bx, by = bullet.position.x, bullet.position.y
    b2 = bullet.position+(bullet.velocity*bullet.ttl)

    (p1x, p1y), (p2x, p2y), (cx, cy) = (bx, by), (b2.x, b2.y), (player.position.x, player.position.y)
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
    discriminant = player.radius ** 2 * dr ** 2 - big_d ** 2
    return discriminant >= 0
