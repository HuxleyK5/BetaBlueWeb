from TVPoke.BaseClasses.PokeTypes import Flying
from TVPoke.BaseClasses.Move import Move
from random import randint

class Taillow(Flying):
    def __init__(self):
        super().__init__("Taillow", 40, [
            Move("Peck", "FLYING", 35),
            Move("Growl", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Wing Attack", "FLYING", 60)
        ], "./TVPoke/Pokemon/imgs/Taillow.png")

class Swellow(Flying):
    def __init__(self):
        super().__init__("Swellow", 60, [
            Move("Peck", "FLYING", 35),
            Move("Growl", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Aerial Ace", "FLYING", 60)
        ], "./TVPoke/Pokemon/imgs/Swellow.png")


