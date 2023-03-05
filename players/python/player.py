from proboj import *
import random

from math import inf
from math import atan2

class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(XY(200 * random.random() - 100, 200 * random.random() - 100), 6.28 * random.random(),
                    random.choice([True, True]), 0, 0)

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

        return Turn(nearest-self.myself.position, atan2((nearest-self.myself.position).y, (nearest-self.myself.position).x),
                    True, 0, 0)

if __name__ == "__main__":
    p = MiskoPlayer()
    p.run()
