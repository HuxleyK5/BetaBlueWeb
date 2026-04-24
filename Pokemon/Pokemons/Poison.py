from TVPoke.BaseClasses.PokeTypes import Poison
from TVPoke.BaseClasses.Move import Move
from random import randint


class Gulpin(Poison):
    def __init__(self):
        super().__init__("Gulpin", 70, [
            Move("Pound", "NORMAL", 40),
            Move("Acid Spray", "POISON", 40),
            Move("Amnesia", "PSYCHIC", 0),
            Move("Sludge Bomb", "POISON", 90)
        ], "./TVPoke/Pokemon/imgs/Gulpin.png")


class Swalot(Poison):
    def __init__(self):
        super().__init__("Swalot", 100, [
            Move("Pound", "NORMAL", 40),
            Move("Acid Spray", "POISON", 40),
            Move("Poison Powder", "POISON", 0),
            Move("Sludge Bomb", "POISON", 90)
        ], "./TVPoke/Pokemon/imgs/Swalot.png")


class Grimer(Poison):
    def __init__(self):
        super().__init__("Grimer", 80, [
            Move("Pound", "NORMAL", 40),
            Move("Poison Gas", "POISON", 0),
            Move("Harden", "NORMAL", 0),
            Move("Mud Bomb", "GROUND", 65)
        ], "./TVPoke/Pokemon/imgs/Grimer.png")


class Muk(Poison):
    def __init__(self):
        super().__init__("Muk", 105, [
            Move("Pound", "NORMAL", 40),
            Move("Poison Gas", "POISON", 0),
            Move("Harden", "NORMAL", 0),
            Move("Gunk Shot", "POISON", 120)
        ], "./TVPoke/Pokemon/imgs/Muk.png")


class Koffing(Poison):
    def __init__(self):
        super().__init__("Koffing", 40, [
            Move("Poison Gas", "POISON", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Smokescreen", "NORMAL", 0),
            Move("Sludge Bomb", "POISON", 90)
        ], "./TVPoke/Pokemon/imgs/Koffing.png")


class Weezing(Poison):
    def __init__(self):
        super().__init__("Weezing", 65, [
            Move("Poison Gas", "POISON", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Sludge Bomb", "POISON", 90),
            Move("Explosion", "NORMAL", 250)
        ], "./TVPoke/Pokemon/imgs/Weezing.png")


class Seviper(Poison):
    def __init__(self):
        super().__init__("Seviper", 73, [
            Move("Scratch", "NORMAL", 40),
            Move("Poison Tail", "POISON", 50),
            Move("Scary Face", "NORMAL", 0),
            Move("Sludge Bomb", "POISON", 90)
        ], "./TVPoke/Pokemon/imgs/Seviper.png")
class Zubat(Poison):
    def __init__(self):
        super().__init__("Zubat", 40, [
            Move("Leech Life", "BUG", 80),
            Move("Supersonic", "NORMAL", 0),
            Move("Astonish", "GHOST", 30),
            Move("Bite", "DARK", 60)
        ], "./TVPoke/Pokemon/imgs/Zubat.png")

class Golbat(Poison):
    def __init__(self):
        super().__init__("Golbat", 75, [
            Move("Leech Life", "BUG", 80),
            Move("Supersonic", "NORMAL", 0),
            Move("Astonish", "GHOST", 30),
            Move("Crunch", "DARK", 80)
        ], "./TVPoke/Pokemon/imgs/Golbat.png")

class Crobat(Poison):
    def __init__(self):
        super().__init__("Crobat", 85, [
            Move("Leech Life", "BUG", 80),
            Move("Supersonic", "NORMAL", 0),
            Move("Astonish", "GHOST", 30),
            Move("Cross Poison", "POISON", 70)
        ], "./TVPoke/Pokemon/imgs/Crobat.png")

