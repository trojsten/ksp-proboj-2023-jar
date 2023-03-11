import math


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

    def distance(self, B):
        return math.sqrt(XY.squared_distace(self, B))

    def __hash__(self):
        return hash((self.x, self.y))
