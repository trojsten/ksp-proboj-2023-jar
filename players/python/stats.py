import enum
from dataclasses import dataclass


class StatsEnum(enum.Enum):
    StatRange = 0
    StatSpeed = 1
    StatBulletSpeed = 2
    StatBulletTTL = 3
    StatBulletDamage = 4
    StatHealthMax = 5
    StatHealthRegeneration = 6
    StatBodyDamage = 7
    StatReloadSpeed = 8
    StatNone = 9


class Stats:
    @staticmethod
    def read_stat_levels():
        stats = []
        for idx, lvl in enumerate(map(int, input().split())):
            stats.append(lvl)
        return stats

    @staticmethod
    def read_stat_values():
        stats = []
        for idx, lvl in enumerate(map(float, input().split())):
            stats.append(lvl)
        return stats
