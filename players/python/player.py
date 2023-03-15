from libs.shoot import *
from libs.proboj import *
from libs.xy import *
import random

from math import inf
from math import atan2


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class MiskoPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        nearest = XY(inf, inf)

        for entity in self.entities:
            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                nearest = entity.position

        for player in self.players.values():
            if player != self.myself:
                self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
                if self.myself.position.distance(player.position) < self.myself.position.distance(nearest) or True:
                    nearest = player.position

        self.log("ideme na", nearest.x, nearest.y)

        if nearest == XY(inf, inf):
            nearest = XY(0, 0)

        return Turn(velocity=nearest - self.myself.position,
                    shoot=OneBulletShoot(atan2((nearest - self.myself.position).y, (nearest - self.myself.position).x)),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


if __name__ == "__main__":
    p = MiskoPlayer()
    p.run()
