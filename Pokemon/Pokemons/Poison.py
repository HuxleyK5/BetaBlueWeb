from TVPoke.BaseClasses.PokeTypes import Poison
from TVPoke.BaseClasses.Move import Move
from random import randint

class Gulpin(Poison):
    def __init__(self):
        moves = [
            Move("Sludge", "POISON", 65),
            Move("Pound", "NORMAL", 40),
            Move("Toxic", "POISON", 0),
            Move("Encore", "NORMAL", 0)
        ]
        super().__init__("Gulpin", 70, moves, "./TVPoke/Pokemon/imgs/Gulpin.png")

class Swalot(Poison):
    def __init__(self):
        moves = [
            Move("Body Slam", "NORMAL", 85),
            Move("Sludge", "POISON", 65),
            Move("Pound", "NORMAL", 40),
            Move("Encore", "NORMAL", 0)
        ]
        super().__init__("Swalot", 100, moves, "./TVPoke/Pokemon/imgs/Swalot.png")

class Grimer(Poison):
    def __init__(self):
        moves = [
            Move("Sludge", "POISON", 65),
            Move("Pound", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Minimize", "NORMAL", 0)
        ]
        super().__init__("Grimer", 80, moves, "./TVPoke/Pokemon/imgs/Grimer.png")

class Muk(Poison):
    def __init__(self):
        moves = [
            Move("Sludge", "POISON", 65),
            Move("Pound", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Minimize", "NORMAL", 0)
        ]
        super().__init__("Muk", 105, moves, "./TVPoke/Pokemon/imgs/Muk.png")

class Koffing(Poison):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Sludge", "POISON", 65),
            Move("Tackle", "NORMAL", 35),
            Move("Smog", "POISON", 20)
        ]
        super().__init__("Koffing", 40, moves, "./TVPoke/Pokemon/imgs/Koffing.png")

class Weezing(Poison):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Sludge", "POISON", 65),
            Move("Tackle", "NORMAL", 35),
            Move("Smog", "POISON", 20)
        ]
        super().__init__("Weezing", 65, moves, "./TVPoke/Pokemon/imgs/Weezing.png")

class Seviper(Poison):
    def __init__(self):
        moves = [
            Move("Crunch", "DARK", 80),
            Move("Bite", "DARK", 60),
            Move("Poison Tail", "POISON", 50),
            Move("Lick", "GHOST", 20)
        ]
        super().__init__("Seviper", 73, moves, "./TVPoke/Pokemon/imgs/Seviper.png")

class Zubat(Poison):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Bite", "DARK", 60),
            Move("Astonish", "GHOST", 30),
            Move("Leech Life", "BUG", 20)
        ]
        super().__init__("Zubat", 40, moves, "./TVPoke/Pokemon/imgs/Zubat.png")

class Golbat(Poison):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Bite", "DARK", 60),
            Move("Astonish", "GHOST", 30),
            Move("Leech Life", "BUG", 20)
        ]
        super().__init__("Golbat", 75, moves, "./TVPoke/Pokemon/imgs/Golbat.png")

class Crobat(Poison):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Bite", "DARK", 60),
            Move("Astonish", "GHOST", 30),
            Move("Leech Life", "BUG", 20)
        ]
        super().__init__("Crobat", 85, moves, "./TVPoke/Pokemon/imgs/Crobat.png")
