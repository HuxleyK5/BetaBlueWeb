from TVPoke.BaseClasses.PokeTypes import Ice
from TVPoke.BaseClasses.Move import Move
from random import randint

class Snorunt(Ice):
    def __init__(self):
        moves = [
            Move("Crunch", "DARK", 80),
            Move("Headbutt", "NORMAL", 70),
            Move("Bite", "DARK", 60),
            Move("Icy Wind", "ICE", 55)
        ]
        super().__init__("Snorunt", 50, moves, "./TVPoke/Pokemon/imgs/Snorunt.png")

class Glalie(Ice):
    def __init__(self):
        moves = [
            Move("Crunch", "DARK", 80),
            Move("Headbutt", "NORMAL", 70),
            Move("Bite", "DARK", 60),
            Move("Icy Wind", "ICE", 55)
        ]
        super().__init__("Glalie", 80, moves, "./TVPoke/Pokemon/imgs/Glalie.png")

class Spheal(Ice):
    def __init__(self):
        moves = [
            Move("Body Slam", "NORMAL", 85),
            Move("Aurora Beam", "ICE", 65),
            Move("Water Gun", "WATER", 40),
            Move("Powder Snow", "ICE", 40)
        ]
        super().__init__("Spheal", 70, moves, "./TVPoke/Pokemon/imgs/Spheal.png")

class Sealeo(Ice):
    def __init__(self):
        moves = [
            Move("Body Slam", "NORMAL", 85),
            Move("Aurora Beam", "ICE", 65),
            Move("Water Gun", "WATER", 40),
            Move("Powder Snow", "ICE", 40)
        ]
        super().__init__("Sealeo", 90, moves, "./TVPoke/Pokemon/imgs/Sealeo.png")

class Walrein(Ice):
    def __init__(self):
        moves = [
            Move("Body Slam", "NORMAL", 85),
            Move("Aurora Beam", "ICE", 65),
            Move("Water Gun", "WATER", 40),
            Move("Powder Snow", "ICE", 40)
        ]
        super().__init__("Walrein", 110, moves, "./TVPoke/Pokemon/imgs/Walrein.png")

class Regice(Ice):
    def __init__(self):
        moves = [
            Move("Explosion", "NORMAL", 250),
            Move("Superpower", "FIGHTING", 120),
            Move("Icy Wind", "ICE", 55),
            Move("Curse", "???", 0)
        ]
        super().__init__("Regice", 80, moves, "./TVPoke/Pokemon/imgs/Regice.png")
