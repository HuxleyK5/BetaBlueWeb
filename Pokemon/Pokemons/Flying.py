from TVPoke.BaseClasses.PokeTypes import Flying
from TVPoke.BaseClasses.Move import Move
from random import randint

class Taillow(Flying):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Quick Attack", "NORMAL", 40),
            Move("Peck", "FLYING", 35),
            Move("Endeavor", "NORMAL", 0)
        ]
        super().__init__("Taillow", 40, moves, "./TVPoke/Pokemon/imgs/Taillow.png")

class Swellow(Flying):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Quick Attack", "NORMAL", 40),
            Move("Peck", "FLYING", 35),
            Move("Endeavor", "NORMAL", 0)
        ]
        super().__init__("Swellow", 60, moves, "./TVPoke/Pokemon/imgs/Swellow.png")
