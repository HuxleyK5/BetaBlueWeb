from TVPoke.BaseClasses.PokeTypes import Ghost
from TVPoke.BaseClasses.Move import Move
from random import randint

class Dusclops(Ghost):
    def __init__(self):
        super().__init__("Dusclops", 40, [
            Move("Leer", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Disable", "NORMAL", 0),
            Move("Shadow Punch", "GHOST", 60)
        ], "./TVPoke/Pokemon/imgs/Dusclops.png")

class Shuppet(Ghost):
    def __init__(self):
        super().__init__("Shuppet", 44, [
            Move("Knock Off", "DARK", 65),
            Move("Screech", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Curse", "GHOST", 0)
        ], "./TVPoke/Pokemon/imgs/Shuppet.png")

class Banette(Ghost):
    def __init__(self):
        super().__init__("Banette", 64, [
            Move("Knock Off", "DARK", 65),
            Move("Screech", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Shadow Claw", "GHOST", 70)
        ], "./TVPoke/Pokemon/imgs/Banette.png")

class Duskull(Ghost):
    def __init__(self):
        super().__init__("Duskull", 20, [
            Move("Leer", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Disable", "NORMAL", 0),
            Move("Astonish", "GHOST", 30)
        ], "./TVPoke/Pokemon/imgs/Duskull.png")
