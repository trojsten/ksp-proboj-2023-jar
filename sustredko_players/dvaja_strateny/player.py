#!/bin/env python3
import random
from math import inf

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(velocity=XY(200 * random.random() - 100, 200 * random.random() - 100),
                    shoot=OneBulletShoot(6.28 * random.random()),
                    stat=StatsEnum.StatNone,
                    new_tank_id=0)


class region(World):
    def __init__(self, min_x, max_x, min_y, max_y):
        super().__init__(min_x, max_x, min_y, max_y)
        self.corners = [XY(min_x, min_y), XY(max_x, min_y), XY(max_x, max_y), XY(min_x, max_y)]
        self.center = XY((max_x - min_x) // 2 + min_x, (max_y - min_y) // 2 + min_y)


class LepsiPlayer(ProbojPlayer):
    def __init__(self):
        super().__init__()
        # self.lsl = -1
        self.aligned: bool = False
        self.current_region: tuple = ()
        self.goal_region: tuple = ()
        self.focus: bool = False
        self.focus_target = None
        self.focus_counter: int = 0
    
    @staticmethod
    def next_region(current: tuple):
        x, y = current
        if x == 0:
            if y == 0: return (1, 0)
            return (0, y - 1)
        if x == 1:
            if y == 0: return (2, 0)
            return (x - 1, y)
        if y == 2: return (1, 2)
        return (2, y + 1)
    
    def when_collide(self, bullet: Bullet, direction: XY) -> int:
        self.log("dodge info - " + str(direction.x) + "     " + str(int(self.myself.stat_values[StatsEnum.StatSpeed])))
        tankVelocity = XY(
            direction.x / math.sqrt(direction.x**2 + direction.y**2) * int(self.myself.stat_values[StatsEnum.StatSpeed]),
            direction.y / math.sqrt(direction.x**2 + direction.y**2) * int(self.myself.stat_values[StatsEnum.StatSpeed])
        )
        tankVelocity = XY(1,1)
        for i in range(1, 6):
            collides = Segment.collides(
                Segment(
                    bullet.position,
                    bullet.position + XY(bullet.velocity.x * i, bullet.velocity.y * i)
                ),
                bullet.radius,
                Segment(
                    self.myself.position,
                    self.myself.position + XY(tankVelocity.x *i, tankVelocity.y * i)
                ),
                self.myself.radius
            )
            if collides: return i
        return -1

    def make_turn(self) -> Turn:
        xbounds = [
            (self.world.min_x, self.world.min_x + (self.world.max_x - self.world.min_x) // 3),
            (self.world.min_x + (self.world.max_x - self.world.min_x) // 3, self.world.max_x - (self.world.max_x - self.world.min_x) // 3),
            (self.world.max_x - (self.world.max_x - self.world.min_x) // 3, self.world.max_x)
        ]

        ybounds = [
            (self.world.min_y, self.world.min_y + (self.world.max_y - self.world.min_y) // 3),
            (self.world.min_y + (self.world.max_y - self.world.min_y) // 3, self.world.max_y - (self.world.max_y - self.world.min_y) // 3),
            (self.world.max_y - (self.world.max_y - self.world.min_y) // 3, self.world.max_y)
        ]

        regions = [
            [region(*xbounds[0], *ybounds[0]), region(*xbounds[1], *ybounds[0]), region(*xbounds[2], *ybounds[0])],
            [region(*xbounds[0], *ybounds[1]), region(*xbounds[1], *ybounds[1]), region(*xbounds[2], *ybounds[1])],
            [region(*xbounds[0], *ybounds[2]), region(*xbounds[1], *ybounds[2]), region(*xbounds[2], *ybounds[2])]
        ]

        if self.myself.tank.tank_id in [0, 5]:
            if self.myself.tank.tank_id == 0: bonuses = (0, 0)
            if self.myself.tank.tank_id == 5: bonuses = (10, 6)
            bspd = self.myself.stat_values[StatsEnum.StatBulletSpeed] + bonuses[0]
            bttl = self.myself.stat_values[StatsEnum.StatBulletTTL] + bonuses[1]
            brch = bspd * bttl
            self.log(f"tank {self.myself.tank.tank_id}")
            self.log(f"brch {brch}")
            self.log(f"range lvl {self.myself.stat_levels[StatsEnum.StatRange]}")
            self.log(f"range val {self.myself.stat_values[StatsEnum.StatRange]}")

            if not self.aligned:
                self.log("aligning")
                shoot = NoShoot()
                nearest = (0, 0)
                for row in range(3):
                    for column in range(3):
                        if [row, column] != [1, 1]:
                            if self.myself.position.distance(regions[row][column].center) < self.myself.position.distance(regions[nearest[0]][nearest[1]].center):
                                nearest = (row, column)
                goal = regions[nearest[0]][nearest[1]].center
                if self.myself.position.x == goal.x and self.myself.position.y == goal.y:
                    self.aligned = True
                    self.current_region = nearest
                    self.goal_region = self.next_region(self.current_region)
                    self.log(f"aligned to {self.current_region[0]} {self.current_region[1]}")
                    self.log(f"continuing to {self.goal_region[0]} {self.goal_region[1]}")
            elif self.myself.position.x == regions[self.goal_region[0]][self.goal_region[1]].center.x:
                if self.myself.position.y == regions[self.goal_region[0]][self.goal_region[1]].center.y:
                    self.current_region = self.goal_region
                    self.goal_region = self.next_region(self.current_region)
                    self.focus = True
                    nearest = XY(inf, inf)
                    for entity in self.entities:
                        if self.myself.position.distance(entity.position) <= brch:
                            if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                                nearest = entity.position
                                self.focus_target = entity
                    if self.focus_target is None: self.focus = False
                    self.log(f"arrived to {self.current_region[0]} {self.current_region[1]}")
                    if self.focus: self.log(f"focusing on entity on {self.focus_target.position.x} {self.focus_target.position.y} after arrival")
                    
            if self.aligned: 
                if not self.focus:
                    goal = regions[self.goal_region[0]][self.goal_region[1]].center
                    shoot = NoShoot()
                else:
                    goal = self.myself.position
                    shoot = OneBulletShoot(self.myself.position.angle_to(self.focus_target.position))
                    if not self.focus_target in self.entities:
                        self.focus_counter += 1
                        if self.focus_counter == 5 or len(self.entities) == 0:
                            self.focus_counter = 0
                            self.focus = False
                            self.focus_target = None
                            goal = regions[self.goal_region[0]][self.goal_region[1]].center
                            shoot = NoShoot()
                            self.log(f"continuing to {self.goal_region[0]} {self.goal_region[1]}")
                        else:
                            nearest = XY(inf, inf)
                            for entity in self.entities:
                                if self.myself.position.distance(entity.position) <= brch:
                                    if self.myself.position.distance(entity.position) < self.myself.position.distance(nearest):
                                        nearest = entity.position
                                        self.focus_target = entity
                            self.log(f"focusing on entity on {self.focus_target.position.x} {self.focus_target.position.y}")

            # for player in self.players.values():
            #     if player != self.myself:
            #         self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
            #         if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
            #             nearest = player.position

            if self.myself.tank.tank_id == 0: update_to = 5
            else: update_to = 7

            velocity = goal - self.myself.position

            closestTime = 10 ** 30

            for bullet in self.bullets:
                try: when = self.when_collide(bullet, velocity)
                except ZeroDivisionError: when = -1
                if when != -1:
                    if when  < closestTime:
                        closestTime = when
                        closestBullet = bullet
		
            if closestTime <= 5:
                velocity = XY(random.randint(0,8000), random.randint(0,8000))

            # if self.myself.stat_levels[StatsEnum.StatBulletSpeed] > self.lsl:
            #     self.log(str(self.myself.tank.tank_id))
            #     self.log(str(self.myself.stat_levels[StatsEnum.StatBulletSpeed]) + "   " + str(self.myself.stat_values[StatsEnum.StatBulletSpeed]))
            #     self.lsl = self.myself.stat_levels[StatsEnum.StatBulletSpeed]

            turn = Turn(velocity = velocity, shoot = shoot, stat = StatsEnum.StatBulletSpeed, new_tank_id = update_to)
        
        else:
            bonuses = (0, 8)
            bspd = self.myself.stat_values[StatsEnum.StatBulletSpeed] + bonuses[0]
            bttl = self.myself.stat_values[StatsEnum.StatBulletTTL] + bonuses[1]
            brch = bspd * bttl

            if self.myself.position.x == regions[self.goal_region[0]][self.goal_region[1]].center.x:
                if self.myself.position.y == regions[self.goal_region[0]][self.goal_region[1]].center.y:
                    self.current_region = self.goal_region
                    self.goal_region = self.next_region(self.current_region)
                    self.focus = True
                    nearest = XY(inf, inf)
                    for player in self.players.values():
                        if self.myself.position.distance(player.position) <= brch:
                            if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                                nearest = player.position
                                self.focus_target = player
                    self.log(f"arrived to {self.current_region[0]} {self.current_region[1]}")
                    self.log(f"focusing on player on {self.focus_target.position.x} {self.focus_target.position.y}")
                    
            if self.aligned: 
                if not self.focus:
                    goal = regions[self.goal_region[0]][self.goal_region[1]].center
                    shoot = NoShoot()
                else:
                    goal = self.myself.position
                    shoot = PlayerShoot(self.focus_target.id)
                    if not self.focus_target in self.players.values() or self.myself.position.distance(self.focus_target.position) > brch:
                        self.focus_counter += 1
                        if self.focus_counter == 2 or len(self.entities) == 0:
                            self.focus_counter = 0
                            self.focus = False
                            self.focus_target = None
                            goal = regions[self.goal_region[0]][self.goal_region[1]].center
                            shoot = NoShoot()
                            self.log(f"continuing to {self.goal_region[0]} {self.goal_region[1]}")
                        else:
                            nearest = XY(inf, inf)
                            for player in self.players.values():
                                if self.myself.position.distance(player.position) <= brch:
                                    if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
                                        nearest = player.position
                                        self.focus_target = player
                            self.log(f"focusing on player on {self.focus_target.position.x} {self.focus_target.position.y}")

            # for player in self.players.values():
            #     if player != self.myself:
            #         self.log("vidim hraca", player.id, "na", player.position.x, player.position.y)
            #         if self.myself.position.distance(player.position) < self.myself.position.distance(nearest):
            #             nearest = player.position

            velocity = goal - self.myself.position

            closestTime = 10 ** 30

            for bullet in self.bullets:
                try: when = self.when_collide(bullet, velocity)
                except ZeroDivisionError: when = -1
                if when != -1:
                    if when  < closestTime:
                        closestTime = when
                        closestBullet = bullet
		
            if closestTime <= 5:
                velocity = XY(random.randint(0,8000), random.randint(0,8000))

            turn = Turn(velocity = velocity, shoot = shoot, stat = StatsEnum.StatRange, new_tank_id = 7)
        


        return turn


if __name__ == "__main__":
    p = LepsiPlayer()
    p.run()
