from TVPoke.BaseClasses.PokeTypes import Ghost
from TVPoke.BaseClasses.Move import Move
from random import randint

class Dusclops(Ghost):
    def __init__(self):
        moves = [
            Move("Pursuit", "DARK", 40),
            Move("Astonish", "GHOST", 30),
            Move("Bind", "NORMAL", 15),
            Move("Confuse Ray", "GHOST", 0)
        ]
        super().__init__("Dusclops", 40, moves, "./TVPoke/Pokemon/imgs/Dusclops.png")

class Shuppet(Ghost):
    def __init__(self):
        moves = [
            Move("Knock Off", "DARK", 20),
            Move("Spite", "GHOST", 0),
            Move("Curse", "???", 0),
            Move("Night Shade", "GHOST", 0)
        ]
        super().__init__("Shuppet", 44, moves, "./TVPoke/Pokemon/imgs/Shuppet.png")

class Banette(Ghost):
    def __init__(self):
        moves = [
            Move("Knock Off", "DARK", 20),
            Move("Spite", "GHOST", 0),
            Move("Screech", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0)
        ]
        super().__init__("Banette", 64, moves, "./TVPoke/Pokemon/imgs/Banette.png")

class Duskull(Ghost):
    def __init__(self):
        moves = [
            Move("Pursuit", "DARK", 40),
            Move("Astonish", "GHOST", 30),
            Move("Confuse Ray", "GHOST", 0),
            Move("Foresight", "NORMAL", 0)
        ]
        super().__init__("Duskull", 20, moves, "./TVPoke/Pokemon/imgs/Duskull.png")
