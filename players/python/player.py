from proboj import *
import random


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Turn:
        return Turn(XY(2 * random.random() - 1, 2 * random.random() - 1), 6.28 * random.random(),
                    random.choice([True, True]), 0, 0)


if __name__ == "__main__":
    p = MyPlayer()
    p.run()
