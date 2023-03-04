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
    """
    Reprezentuje ťah v hre. Hráč vracia rýchlosť, smer, ktorým sa chce pohnúť,
    či chce vystreliť, ktorý Stat chce updatnúť a id tanku, ktorý by chcel mať.
    """
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
    """
    Trieda, ktorá reprezentuje bod/vektor v 2D.
    Mohla by mať rozuné metódy ako skalárny súčín, sčítavanie vektorov a násobenie skalárom.
    """
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
    """
    Trieda, ktorá reprezentuje bežného hráča v hre.
    * idx - jeho idčko
    * alive - bool, či hráč žije. Snáď by ste ani nemali dostať nie alive hráča.
    * position - XY hráča
    * angle - uhol, kam je aktuálne natočená hlaveň
    * radius - polomer hráča
    * health - health
    """
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

    def merge(self, player: "Player"):
        self.id = player.id
        self.alive = player.alive
        self.position = player.position
        self.angle = player.angle
        self.radius = player.radius
        self.tank = player.tank
        self.health = player.health

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class MyPlayer(Player):
    """
    Trieda, ktorá reprezentuje Tvojho hráča v hre.
    * exp - získané XPčka
    * level - ktorý si záskal
    * levels_left - koľko levelov môžeš ešte použiť na vylepšovanie
    * tank_updates_left - koľko updatov tankov môžeš ešte použiť
    * reload_cooldown - koľko tickcov ešte nemôžeš strieľať
    * lifes_left - koľko respawnov ešte máš
    * stat_levels - aké sú aktuálne levely Tvojich statov
    * stat_values - aké sú aktuálne hodnoty Tvojich statov
    """
    exp: int
    level: int
    levels_left: int
    tank_updates_left: int
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
    """
    Táto trieda vykonáva ťahy v hre
    * world - objekt, ktorý reprezentuje svet
    * myself - Ty
    * _myself - Tvoje id
    * players - `dictionary` hráčov `{id: Player}`
    * bullets - `set` projektilov
    * entities - `set` entít
    """
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
        """
        Načíta info o sebe
        """
        self.myself = MyPlayer.read_myplayer()
        self._myself = self.myself.id

    def _read_players(self):
        """
        Načíta hráčov v dosahu hráča
        """
        self.players = {}
        n = int(input())
        for i in range(n):
            player = Player.read_player()
            self.players[player.id] = player

        self.myself.merge(self.players[self._myself])

    def _read_bullets(self):
        """
        Načíta projektily v dosahu hráča
        """
        self.bullets = set()
        n = int(input())
        for i in range(n):
            bullet = Bullet.read_bullet()
            self.bullets.add(bullet)

    def _read_entities(self):
        """
        Načíta entity v dosahu hráča
        """
        self.entities = set()
        n = int(input())
        for i in range(n):
            entity = Entity.read_entity()
            self.entities.add(entity)

    def _read_turn(self):
        """
        Načíta vstup pre hráča
        """
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
    """
    Projektil:
    * position - `XY`, pozícia
    * velocity - `XY`, rýchlosť
    * shooter_id - id strelca, kľúč do poľa hráčov
    * ttl - koľko tickov ešte projektil bude existovať
    * damage - koľko damage spôsobí pri hite
    """
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
    """
    Entita:
    * position - `XY`, pozícia
    * radius - polomer
    """
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
    """
    World:
    * size - veľkosť mapy, v oboch rozmeroch je to od `+size` do `-size`
    """
    def __init__(self):
        self.size: float = 0

    def read_world(self):
        self.size = float(input())
