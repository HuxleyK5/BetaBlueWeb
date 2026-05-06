from TVPoke.BaseClasses.PokeTypes import Bug
from TVPoke.BaseClasses.Move import Move

class Wurmple(Bug):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 35),
            Move("Poison Sting", "POISON", 15),
            Move("String Shot", "BUG", 0)
        ]
        super().__init__("Wurmple", 45, moves, "./TVPoke/Pokemon/imgs/Wurmple.png")

class Silcoon(Bug):
    def __init__(self):
        moves = [
            Move("Harden", "NORMAL", 0)
        ]
        super().__init__("Silcoon", 50, moves, "./TVPoke/Pokemon/imgs/Silcoon.png")

class Beautifly(Bug):
    def __init__(self):
        moves = [
            Move("Mega Drain", "GRASS", 40),
            Move("Gust", "FLYING", 40),
            Move("Absorb", "GRASS", 20),
            Move("Whirlwind", "NORMAL", 0)
        ]
        super().__init__("Beautifly", 60, moves, "./TVPoke/Pokemon/imgs/Beautifly.png")

class Cascoon(Bug):
    def __init__(self):
        moves = [
            Move("Harden", "NORMAL", 0)
        ]
        super().__init__("Cascoon", 50, moves, "./TVPoke/Pokemon/imgs/Cascoon.png")

class Dustox(Bug):
    def __init__(self):
        moves = [
            Move("Psybeam", "PSYCHIC", 65),
            Move("Confusion", "PSYCHIC", 50),
            Move("Gust", "FLYING", 40),
            Move("Whirlwind", "NORMAL", 0)
        ]
        super().__init__("Dustox", 60, moves, "./TVPoke/Pokemon/imgs/Dustox.png")

class Surskit(Bug):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Quick Attack", "NORMAL", 40),
            Move("Bubble", "WATER", 20),
            Move("Water Sport", "WATER", 0)
        ]
        super().__init__("Surskit", 40, moves, "./TVPoke/Pokemon/imgs/Surskit.png")

class Masquerain(Bug):
    def __init__(self):
        moves = [
            Move("Gust", "FLYING", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Bubble", "WATER", 20),
            Move("Water Sport", "WATER", 0)
        ]
        super().__init__("Masquerain", 70, moves, "./TVPoke/Pokemon/imgs/Masquerain.png")

class Nincada(Bug):
    def __init__(self):
        moves = [
            Move("False Swipe", "NORMAL", 40),
            Move("Scratch", "NORMAL", 40),
            Move("Leech Life", "BUG", 20),
            Move("Fury Swipes", "NORMAL", 18)
        ]
        super().__init__("Nincada", 31, moves, "./TVPoke/Pokemon/imgs/Nincada.png")

class Ninjask(Bug):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Leech Life", "BUG", 20),
            Move("Fury Swipes", "NORMAL", 18),
            Move("Fury Cutter", "BUG", 10)
        ]
        super().__init__("Ninjask", 61, moves, "./TVPoke/Pokemon/imgs/Ninjask.png")

class Shedinja(Bug):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Leech Life", "BUG", 20),
            Move("Fury Swipes", "NORMAL", 18),
            Move("Spite", "GHOST", 0)
        ]
        super().__init__("Shedinja", 1, moves, "./TVPoke/Pokemon/imgs/Shedinja.png")

class Volbeat(Bug):
    def __init__(self):
        moves = [
            Move("Signal Beam", "BUG", 75),
            Move("Quick Attack", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Protect", "NORMAL", 0)
        ]
        super().__init__("Volbeat", 65, moves, "./TVPoke/Pokemon/imgs/Volbeat.png")

class Illumise(Bug):
    def __init__(self):
        moves = [
            Move("Quick Attack", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Flatter", "DARK", 0),
            Move("Encore", "NORMAL", 0)
        ]
        super().__init__("Illumise", 65, moves, "./TVPoke/Pokemon/imgs/Illumise.png")

class Pinsir(Bug):
    def __init__(self):
        moves = [
            Move("Revenge", "FIGHTING", 60),
            Move("ViceGrip", "NORMAL", 55),
            Move("Bind", "NORMAL", 15),
            Move("Harden", "NORMAL", 0)
        ]
        super().__init__("Pinsir", 65, moves, "./TVPoke/Pokemon/imgs/Pinsir.png")

class Heracross(Bug):
    def __init__(self):
        moves = [
            Move("Brick Break", "FIGHTING", 75),
            Move("Horn Attack", "NORMAL", 65),
            Move("Tackle", "NORMAL", 35),
            Move("Fury Attack", "NORMAL", 15)
        ]
        super().__init__("Heracross", 80, moves, "./TVPoke/Pokemon/imgs/Heracross.png")

class Armaldo(Bug):
    def __init__(self):
        moves = [
            Move("Metal Claw", "STEEL", 50),
            Move("Water Gun", "WATER", 40),
            Move("Scratch", "NORMAL", 40),
            Move("Mud Sport", "GROUND", 0)
        ]
        super().__init__("Armaldo", 75, moves, "./TVPoke/Pokemon/imgs/Armaldo.png")
