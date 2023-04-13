#!/bin/env python3
import math
import random
from math import inf
from math import *

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class SamoHrac(ProbojPlayer):
    numOfQuadrants = 6
    quadrantShift = 2

    def velocity(self):
        return self.myself.stat_values[StatsEnum.StatSpeed]

    def range(self):
        return self.myself.stat_values[StatsEnum.StatRange]

    def nearestStuff(self, listOfStuff):
        nearest = None
        for entity in listOfStuff:
            if (self.myself.position == entity.position):
                continue
            if nearest is None or XY.distance(self.myself.position, entity.position) < XY.distance(self.myself.position,
                                                                                                   nearest.position):
                nearest = entity
        if nearest is not None and XY.distance(nearest.position, self.myself.position) > 200:
            return None
        return nearest

    def getQuadrant(self, pos):
        angle = XY.angle_to(self.myself.position, pos) + math.pi
        angle = (angle / (2 * math.pi)) * self.numOfQuadrants
        return floor(angle)

    def getAngles(self, quadrant):
        angle1 = (quadrant * (2 * math.pi)) / self.numOfQuadrants - math.pi
        angle2 = ((quadrant + 1) * (2 * math.pi)) / self.numOfQuadrants - math.pi

        return (angle1, angle2)

    def positionOutOfMap(self, pos: XY):
        return (pos.x > self.world.max_x or pos.x < self.world.min_x
                or pos.y > self.world.max_y or pos.y < self.world.min_y)

    def evalQuadrants(self):
        # index 0 - dobre, index  - zle
        listOfStuff = []
        for i in range(self.numOfQuadrants):
            listOfStuff.append([0, 0])

        for entity in self.entities:
            if (self.positionOutOfMap(entity.position)):
                continue
            if (XY.distance(self.myself.position, entity.position) > (
                    self.velocity() + self.myself.radius + entity.radius)):
                listOfStuff[self.getQuadrant(entity.position)][0] += 5
            else:
                listOfStuff[self.getQuadrant(entity.position)][1] += 1

        for player in self.players.values():
            if player != self.myself:
                q = self.getQuadrant(player.position)
                if (player.health < self.myself.health and XY.distance(self.myself.position,
                                                                       player.position) > self.velocity() * 2):
                    listOfStuff[q][0] += 7
                else:
                    listOfStuff[q][1] += 1

        for bullet in self.bullets:
            pos = bullet.position + bullet.velocity
            if (XY.distance(self.myself.position, pos) <= self.velocity()):
                q = self.getQuadrant(pos)
                listOfStuff[q][1] += 5

        for i in range(self.numOfQuadrants):
            angle = sum(self.getAngles(i)) / 2
            heading = XY(2 * self.velocity() * math.cos(angle), 2 * self.velocity() * math.sin(angle))
            if (self.positionOutOfMap(heading + self.myself.position)):
                listOfStuff[i][1] += 15

        return listOfStuff

    def make_turn(self) -> Turn:
        upgradeable = [StatsEnum.StatSpeed, StatsEnum.StatSpeed, StatsEnum.StatBulletDamage, StatsEnum.StatBulletDamage,
                       StatsEnum.StatBulletDamage, StatsEnum.StatRange, StatsEnum.StatBulletTTL,
                       StatsEnum.StatHealthRegeneration,
                       StatsEnum.StatHealthMax]
        attack = XY(inf, inf)

        nearestEntity = self.nearestStuff(self.entities)
        nearestTank = self.nearestStuff(self.players.values())

        quadrants = self.evalQuadrants()
        hamminess = []
        mostHammedQuadrant = 0

        for q in range(self.numOfQuadrants):
            hamminess.append(quadrants[q][0] + quadrants[(q + self.quadrantShift) % self.numOfQuadrants][1])
            if (hamminess[q] > hamminess[mostHammedQuadrant]):
                mostHammedQuadrant = q

        angle = random.uniform(self.getAngles(mostHammedQuadrant)[0], self.getAngles(mostHammedQuadrant)[1])

        heading = XY(4000 * math.cos(angle), 4000 * math.sin(angle))

        if (hamminess[mostHammedQuadrant] == 0):
            heading = XY(0, 0) - self.myself.position
        self.log(nearestTank, nearestEntity)
        if (nearestTank is not None):
            attack = nearestTank.position
        elif (nearestEntity is not None):
            attack = nearestEntity.position
        else:
            attack = XY(0, 0) - heading
        self.log(self.myself.tank.tank_id)
        return Turn(velocity=heading,
                    shoot=OneBulletShoot(self.myself.position.angle_to(attack)),
                    stat=random.choice(upgradeable),
                    new_tank_id=random.choice((1, 4)))


if __name__ == "__main__":
    p = SamoHrac()
    p.run()
