from TVPoke.BaseClasses.PokeTypes import Ice
from TVPoke.BaseClasses.Move import Move
from random import randint


class Snorunt(Ice):
    def __init__(self):
        super().__init__("Snorunt", 50, [
            Move("Powder Snow", "ICE", 40),
            Move("Leer", "NORMAL", 0),
            Move("Double Team", "NORMAL", 0),
            Move("Ice Beam", "ICE", 90)
        ], "./TVPoke/Pokemon/imgs/Snorunt.png")


class Glalie(Ice):
    def __init__(self):
        super().__init__("Glalie", 80, [
            Move("Powder Snow", "ICE", 40),
            Move("Leer", "NORMAL", 0),
            Move("Bite", "DARK", 60),
            Move("Blizzard", "ICE", 110)
        ], "./TVPoke/Pokemon/imgs/Glalie.png")


class Spheal(Ice):
    def __init__(self):
        super().__init__("Spheal", 70, [
            Move("Powder Snow", "ICE", 40),
            Move("Growl", "NORMAL", 0),
            Move("Water Gun", "WATER", 40),
            Move("Icy Wind", "ICE", 55)
        ], "./TVPoke/Pokemon/imgs/Spheal.png")


class Sealeo(Ice):
    def __init__(self):
        super().__init__("Sealeo", 90, [
            Move("Powder Snow", "ICE", 40),
            Move("Growl", "NORMAL", 0),
            Move("Aurora Beam", "ICE", 65),
            Move("Blizzard", "ICE", 110)
        ], "./TVPoke/Pokemon/imgs/Sealeo.png")


class Walrein(Ice):
    def __init__(self):
        super().__init__("Walrein", 110, [
            Move("Ice Fang", "ICE", 65),
            Move("Body Slam", "NORMAL", 85),
            Move("Surf", "WATER", 90),
            Move("Blizzard", "ICE", 110)
        ], "./TVPoke/Pokemon/imgs/Walrein.png")


class Regice(Ice):
    def __init__(self):
        super().__init__("Regice", 80, [
            Move("Curse", "GHOST", 0),
            Move("Superpower", "FIGHTING", 120),
            Move("Ice Beam", "ICE", 90),
            Move("Blizzard", "ICE", 110)
        ], "./TVPoke/Pokemon/imgs/Regice.png")
