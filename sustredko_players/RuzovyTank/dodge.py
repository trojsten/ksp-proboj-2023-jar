import random
from math import inf
import math

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


def dodge_bullet(self: ProbojPlayer, bullet: Bullet) -> XY:
    return XY(bullet.velocity.y, -bullet.velocity.x)


def dodge_strategy(self: ProbojPlayer, desired_direction: XY):
    for angle_delta in range(0, 314, 2):
        res = check_angle(self, desired_direction, angle_delta / 100)
        if res:
            return res
        resn = check_angle(self, desired_direction, -angle_delta / 100)
        if resn:
            return resn
    self.log("No good direction found.")
    return desired_direction


def check_angle(self: ProbojPlayer, desired_direction: XY, angle: float):
    new_vector = XY(
        math.cos(angle) * desired_direction.x - math.sin(angle) * desired_direction.y,
        math.sin(angle) * desired_direction.x + math.cos(angle) * desired_direction.y,
    )

    pos = self.myself.position + new_vector
    bad = False
    for bullet in self.bullets:
        if bullet.shooter_id == self.myself.id:
            continue
        future_pos = bullet.position + bullet.velocity * bullet.ttl  # TODO adjust

        if Segment.collides(
            Segment(pos, pos),
            self.myself.radius,
            Segment(bullet.position, future_pos),
            bullet.radius,
        ):
            bad = True
            break
    if not bad:
        return new_vector
    else:
        return False
