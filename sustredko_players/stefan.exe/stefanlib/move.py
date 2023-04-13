from libs.geometry import *
from libs.proboj import *
from libs.shoot import *
from random import randint

from stefanlib.utils import *


def get_move_target(self: ProbojPlayer) -> XY:
    w = self.world
    e = nearest_entity(self)
    p = nearest_player(self)
    pos = self.myself.position
    mid = XY((w.min_x+w.max_x)/2, (w.min_y+w.max_y)/2)
    rad = self.myself.stat_values[StatsEnum.StatRange]
    vel = self.myself.stat_values[StatsEnum.StatSpeed] * 2
    size = self.myself.radius

    x, y = 0, 0

    b = threatening_bullet(self)
    if b is not None:
        self.log(f"DODGE")
        x, y = b.velocity.y, -b.velocity.x

    # Border x
    BORDER_AVOIDANCE = 60
    if abs(pos.x-w.min_x) < size * BORDER_AVOIDANCE:
        self.log(f"BORDER DODGE XMIN")
        x = w.max_x
    elif abs(pos.x-w.max_x) < size * BORDER_AVOIDANCE:
        self.log(f"BORDER DODGE XMAX")
        x = w.min_x
    # Border y
    if abs(pos.y-w.min_y) < size * BORDER_AVOIDANCE:
        self.log(f"BORDER DODGE YMIN")
        y = w.max_y
    elif abs(pos.y-w.max_y) < size * BORDER_AVOIDANCE:
        self.log(f"BORDER DODGE YMAX")
        y = w.min_y

    # nearest entity
    if e is not None:
        if e.position.distance(pos) > 4*(size+e.radius):
            if x == 0:
                self.log(f"ENTITY X")
                x = e.position.x
            if y == 0:
                self.log(f"ENTITY Y")
                y = e.position.y

    # 20%
    TOLERANCE = .2
    if not (abs((w.min_x-rad*.2)-pos.x) < rad*TOLERANCE\
            or abs((w.max_x-rad*.2)-pos.x) < rad*TOLERANCE):
        if x == 0:
            if pos.x < mid.x/2:
                self.log(f"BRODER EDGE XMIN")
                x = w.min_x - rad * .2
            else:
                self.log(f"BRODER EDGE XMAX")
                x = w.max_x + rad * .2
    if not (abs((w.min_y - rad * .2) - pos.y) < rad *TOLERANCE \
                or abs((w.max_y - rad * .2) - pos.y) < rad *TOLERANCE):
        if y == 0:
            if pos.y < mid.y/2:
                self.log(f"BRODER EDGE YMIN")
                y = w.min_y - rad * .2
            else:
                self.log(f"BRODER EDGE YMAX")
                y = w.max_y + rad * .2

    # Bored
    if x == 0:
        if abs(w.min_x-pos.x) > abs(w.max_x-pos.x):
            x = w.min_x
            self.log(f"BORED MINX")
        else:
            self.log(f"BORED MAXX")
            x = w.max_x
    if y == 0:
        if abs(w.min_y - pos.y) > abs(w.max_y - pos.y):
            self.log(f"BORED MINY")
            y = w.min_y
        else:
            self.log(f"BORED MAXY")
            y = w.max_y

    return XY(x, y)
    # XY(randint(int(w.min_x), int(w.max_x)), randint(int(w.min_y), int(w.max_y)))


def get_move_vector(target: XY, self: ProbojPlayer) -> XY:
    return target - self.myself.position
