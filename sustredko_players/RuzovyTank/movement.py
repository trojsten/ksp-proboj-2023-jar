import random
from math import inf
from parameter_array_enum import ParameterEnum
from parameters import parameters

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

NUM_TRIED_VECTORS_FULL = 100
NUM_TRIED_VECTORS_SCALED = 100



def adjust_move(self: ProbojPlayer, desired_move: XY):
    if desired_move.distance(XY(0, 0)) == 0:
        return desired_move
    moves = []
    self.log(desired_move)
    desired_move *= min(
        1,
        self.myself.stat_values[StatsEnum.StatSpeed] / desired_move.distance(XY(0, 0)),
    )
    for i in range(NUM_TRIED_VECTORS_FULL):
        moves.append(get_vector(self, desired_move))

    for i in range(NUM_TRIED_VECTORS_SCALED):
        moves.append(get_vector(self, desired_move, random.random()))

    moves.sort(key=lambda x: x[0])

    self.log(f"Picked move {moves[0][1]}, error {moves[0][0]}. Desired:{desired_move}")
    # self.log(f"Possible moves: {moves}")
    vector_error(self, desired_move, moves[0][1], True)
    return moves[0][1]


def get_vector(
    self: ProbojPlayer, desired_move: XY, scale: float = 1
) -> tuple[float, XY]:
    vector = XY(random.random() * 2 - 1, random.random() * 2 - 1)
    vector *= self.myself.stat_values[StatsEnum.StatSpeed] / vector.distance(XY(0, 0))

    vector *= scale

    return (vector_error(self, desired_move, vector), vector)


ZONE_SAFE_DIST = 50


def vector_error(self: ProbojPlayer, desired_move: XY, vector: XY, print_debug=False):
    error_vector_difference = (
        vector_difference(desired_move, vector)
        / self.myself.stat_values[StatsEnum.StatSpeed]
    )

    pos = self.myself.position + vector
    error_bullet = 0
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
            error_bullet += (
                bullet.damage * self.parameters[ParameterEnum.BulletDamageFactor]
            )

    error_entity_collision = 0
    for entity in self.entities:
        if pos.distance(entity.position) < self.myself.radius + entity.radius:
            error_entity_collision += self.parameters[ParameterEnum.EntityTouchDanger]

    error_close_player = 0
    for player in self.players.values():
        if pos.distance(player.position) < self.gun_range - 5:
            error_close_player += pow(
                (self.gun_range - pos.distance(player.position) - 5)
                * self.parameters[ParameterEnum.PlayerDanger],
                1,
            )

    error_edge = edge_error(self, pos)

    if error_edge > 1e10:
        return inf

    error = (
        error_vector_difference
        + error_bullet
        + error_entity_collision
        + error_edge
        + error_close_player
    )
    if print_debug:
        self.log(
            f"ERRORS: vector difference {error_vector_difference}, bullet {error_bullet}, entity collision {error_entity_collision}, edge {error_edge}, close player {error_close_player}"
        )
    return error


def edge_error(self: ProbojPlayer, pos: XY):
    error = 0
    const = self.parameters[ParameterEnum.EdgeDanger]

    dist = self.world.min_x - pos.x + ZONE_SAFE_DIST
    if dist > 0:
        error += const * dist

    dist = self.world.min_y - pos.y + ZONE_SAFE_DIST
    if dist > 0:
        error += const * dist

    dist = -self.world.max_x + pos.x + ZONE_SAFE_DIST
    if dist > 0:
        error += const * dist

    dist = -self.world.max_y + pos.y + ZONE_SAFE_DIST
    if dist > 0:
        error += const * dist

    error /= self.myself.stat_values[StatsEnum.StatSpeed]
    return error**5


def vector_difference(desired_move: XY, vector: XY):
    return (
        desired_move.distance(vector)
        * parameters[ParameterEnum.VectorDifferenceErrorConstant]
    )
