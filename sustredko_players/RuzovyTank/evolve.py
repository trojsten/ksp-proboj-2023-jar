import random
from math import inf
import math

from libs.geometry import *
from libs.proboj import *
from libs.shoot import *

@dataclass
class Strategy:
    @staticmethod
    def get_strategies():
        return [
            Heavy(),
            Sniper(),
            MachineGun(),
            Guided()
        ]
    def get_strategy(id:int):
        for ss in Strategy.get_strategies():
            if ss.id==id:
                return ss

    @abstractmethod
    def id(self) -> int:
        pass

    @abstractmethod
    def endpoint(self) -> int:
        pass

    @abstractmethod
    def upgrade_strategy(self) -> List:
        pass
@dataclass
class Heavy(Strategy):
    id = 1
    endpoint = 6
    upgrade_strategy=[
        StatsEnum.StatHealthMax,
        StatsEnum.StatHealthRegeneration,
        StatsEnum.StatBulletDamage,
        StatsEnum.StatRange
    ]
@dataclass
class Sniper(Strategy):
    id = 2
    endpoint = 6
    upgrade_strategy=[
        StatsEnum.StatBulletDamage,
        StatsEnum.StatRange,
        StatsEnum.StatBulletTTL
    ]

@dataclass
class MachineGun(Strategy):
    id = 3
    endpoint = 8
    upgrade_strategy=[
        StatsEnum.StatReloadSpeed,
        StatsEnum.StatRange,
        StatsEnum.StatSpeed
    ]

@dataclass
class Guided(Strategy):
    id = 4
    endpoint = 7
    upgrade_strategy=[
        StatsEnum.StatBulletDamage,
        StatsEnum.StatRange,
        StatsEnum.StatBulletTTL
    ]


def chose_stat(self):
    strategy= self.my_strategy
    if self.myself.stat_values[StatsEnum.StatBulletTTL]<3:
        return StatsEnum.StatBulletTTL
    valid=[]
    for stat in strategy.upgrade_strategy:
        if self.myself.stat_levels[stat]<7:
            valid.append(stat)
    if len(valid)!=0:
        chosen = random.choice(valid) 
        return chosen
    all_stats = [
        StatsEnum.StatRange,
        StatsEnum.StatSpeed,
        StatsEnum.StatBulletTTL,
        StatsEnum.StatBulletDamage,
        StatsEnum.StatReloadSpeed,
        StatsEnum.StatHealthMax,
        StatsEnum.StatHealthRegeneration,
        StatsEnum.StatBulletSpeed,
        StatsEnum.StatBodyDamage
        
    ]
    for stat in all_stats:
        if self.myself.stat_levels[stat]<7:
            return stat
    return StatsEnum.StatNone

def chose_evolution(self:ProbojPlayer)-> int:
    desired_endpoint=self.my_strategy.endpoint
    for tank in self.myself.tank.updatable_to:
        if tank.tank_id == desired_endpoint:
            self.log("desired reached")
            return tank.tank_id
        for next_tank in tank.updatable_to:
            if next_tank.tank_id==desired_endpoint:
                return tank.tank_id

    return 0