import sys
from dataclasses import dataclass
import math
from typing import List, Type, Set

from tanks import *
from stats import *

_input = input


def lepsiInput():
    d = _input()
    print(d, file=sys.stderr)
    return d


input = lepsiInput


class Turn:
    def __init__(self, velocity, angle: float, shoot: bool, stat: int, new_tank_id: int):
        self.x = float(velocity.x)
        self.y = float(velocity.y)
        self.angle = float(angle)
        self.shoot = int(shoot)
        self.stat = int(stat)
        self.new_tank_id = int(new_tank_id)

    def print(self):
        print(f"{self.x} {self.y} {self.angle} {self.shoot} {self.stat} {self.new_tank_id}")
        print(".")


class XY:

    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y

    @staticmethod
    def dot(v, u):
        return v.x * u.x + v.y * u.y

    def __sub__(self, other):
        return XY(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return XY(self.x * other, self.y * other)
        raise ArithmeticError(f"Cannot multiply by {type(other)}")

    @staticmethod
    def squared_distace(A, B):
        d = A - B
        return d.x * d.x + d.y * d.y

    @staticmethod
    def distance(A, B):
        return math.sqrt(XY.squared_distace(A, B))


@dataclass
class Player:
    id: int
    alive: bool
    position: XY
    angle: float
    radius: float
    tank: Tank
    health: float

    @classmethod
    def read_player(cls) -> Type["Player"]:
        id, alive, x, y, angle, radius, tank_id, health = input().split()
        player = Player
        player.id = int(id)
        player.alive = bool(int(alive))
        player.position = XY(float(x), float(y))
        player.angle = float(angle)
        player.radius = float(radius)
        player.tank = Tank.get_tank(int(tank_id))
        player.health = float(health)
        return player

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class MyPlayer(Player):
    exp: int
    level: int
    tank_updates_left: int
    levels_left: int
    reload_cooldown: int
    lifes_left: int
    stat_levels: List[int]
    stat_values: List[float]

    @classmethod
    def read_myplayer(cls) -> Type["MyPlayer"]:
        id, exp, level, levels_left, tank_updates_left, reload_cooldown, lifes_left = input().split()
        myplayer = MyPlayer
        myplayer.id = int(id)
        myplayer.exp = int(exp)
        myplayer.level = int(level)
        myplayer.levels_left = int(levels_left)
        myplayer.tank_updates_left = int(tank_updates_left)
        myplayer.reload_cooldown = int(reload_cooldown)
        myplayer.lifes_left = int(lifes_left)
        myplayer.stat_levels = Stats.read_stat_levels()
        myplayer.stat_values = Stats.read_stat_values()
        return myplayer


class ProbojPlayer:
    def __init__(self):
        self.world: World = World()
        self.myself: MyPlayer
        self._myself: int
        self.players: dict[int: Player] = {}
        self.bullets: Set[Bullet] = set()
        self.entities: Set[Entity] = set()

    @staticmethod
    def log(*args):
        """
        Vypíše dáta do logu. Syntax je rovnaká ako print().
        """
        print(*args, file=sys.stderr)

    def _read_myself(self):
        self.myself = MyPlayer.read_myplayer()
        self._myself = self.myself.id

    def _read_players(self):
        self.players = {}
        n = int(input())
        for i in range(n):
            player = Player.read_player()
            self.players[player.id] = player

    def _read_bullets(self):
        self.bullets = set()
        n = int(input())
        for i in range(n):
            bullet = Bullet.read_bullet()
            self.bullets.add(bullet)

    def _read_entities(self):
        self.entities = set()
        n = int(input())
        for i in range(n):
            entity = Entity.read_entity()
            self.entities.add(entity)

    def _read_turn(self):
        self.world.read_world()
        self._read_myself()
        self._read_players()
        self._read_bullets()
        self._read_entities()
        input()
        input()

    def _send_turns(self, turn: Turn):
        """
        Odošle ťah serveru.
        """
        turn.print()

    def make_turn(self) -> Turn:
        """
        Vykoná ťah.
        Funkcia vracia objekt Turn
        """
        raise NotImplementedError()

    def run(self):
        """
        Hlavný cyklus hry.
        """
        while True:
            self._read_turn()
            turns = self.make_turn()
            self._send_turns(turns)


@dataclass
class Bullet:
    position: XY
    velocity: XY
    shooter_id: int
    ttl: float
    damage: float

    @classmethod
    def read_bullet(cls) -> Type["Bullet"]:
        x, y, vx, vy, shooter_id, ttl, damage = input().split()
        bullet = Bullet
        bullet.position = XY(float(x), float(y))
        bullet.velocity = XY(float(vx), float(vy))
        bullet.shooter_id = int(shooter_id)
        bullet.ttl = float(ttl)
        bullet.damage = float(damage)
        return bullet


@dataclass
class Entity:
    position: XY
    radius: float

    @classmethod
    def read_entity(cls) -> Type["Entity"]:
        x, y, radius = input().split()
        entity = Entity
        entity.position = XY(float(x), float(y))
        entity.radius = float(radius)
        return entity


class World:

    def __init__(self):
        self.size: float = 0
        self.players: List[Player] = []
        self.bullets: List[Bullet] = []
        self.entities: List[Entity] = []

    def read_world(self):
        self.size = float(input())
