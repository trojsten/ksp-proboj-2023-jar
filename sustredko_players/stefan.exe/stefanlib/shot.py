from math import inf, pi

from libs.geometry import *
from typing import Union
from libs.proboj import *
from libs.shoot import *
from random import randint
from stefanlib.utils import nearest_entity, nearest_player, my_shoot_range


def get_shot(self: ProbojPlayer) -> Shoot:
    if self.myself.reload_cooldown > 0:
        return NoShoot()

    entity = nearest_entity(self, my_shoot_range(self))
    player = nearest_player(self, my_shoot_range(self))
    target = player or entity
    guided = self.myself.tank.tank_id == 7

    ## Guided
    if player is not None and guided:
        self.log(f"{player.id}]Player shoot {player.id}")
        return PlayerShoot(player.id)
    ##

    if target is None:
        self.log(f"Nemam target ============")
        return NoShoot()

    if guided:
        return XyShoot(target.position)
    else:
        # angle = 2*pi * randint(0, 100)/100
        angle = self.myself.position.angle_to(target.position)
        self.log(f"{self.myself.position}]Shooting entity {target} ({type(target)}, {target.position}) with angle, ttl{self.myself.stat_values[StatsEnum.StatBulletTTL]} ==========")
        return OneBulletShoot(angle)
