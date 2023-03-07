from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Tank(ABC):
    @staticmethod
    def get_tank(id: int):
        if id == BasicTank.tank_id:
            return BasicTank()
        return None

    @abstractmethod
    def tank_id(self) -> int:
        pass

    @abstractmethod
    def updatable_to(self) -> List:
        pass


@dataclass
class BasicTank(Tank):
    tank_id = 0
    updatable_to = []
