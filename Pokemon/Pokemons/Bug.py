from TVPoke.BaseClasses.PokeTypes import Bug
from TVPoke.BaseClasses.Move import Move

class Wurmple(Bug):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("String Shot", "BUG", 0),
            Move("Poison Sting", "POISON", 15),
            Move("Bug Bite", "BUG", 60)
        ]
        super().__init__("Wurmple", 45, moves, "./TVPoke/Pokemon/imgs/Wurmple.png")

class Silcoon(Bug):
    def __init__(self):
        moves = [
            Move("Harden", "NORMAL", 0),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Silcoon", 50, moves, "./TVPoke/Pokemon/imgs/Silcoon.png")

class Beautifly(Bug):
    def __init__(self):
        moves = [
            Move("Absorb", "GRASS", 20),
            Move("Gust", "FLYING", 40),
            Move("Stun Spore", "GRASS", 0),
            Move("Morning Sun", "NORMAL", 0)
        ]
        super().__init__("Beautifly", 60, moves, "./TVPoke/Pokemon/imgs/Beautifly.png")

class Cascoon(Bug):
    def __init__(self):
        moves = [
            Move("Harden", "NORMAL", 0),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Cascoon", 50, moves, "./TVPoke/Pokemon/imgs/Cascoon.png")

class Dustox(Bug):
    def __init__(self):
        moves = [
            Move("Gust", "FLYING", 40),
            Move("Confusion", "PSYCHIC", 50),
            Move("Poison Powder", "POISON", 0),
            Move("Moonlight", "NORMAL", 0)
        ]
        super().__init__("Dustox", 60, moves, "./TVPoke/Pokemon/imgs/Dustox.png")

class Surskit(Bug):
    def __init__(self):
        moves = [
            Move("Bubble", "WATER", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Sweet Scent", "NORMAL", 0),
            Move("Water Sport", "WATER", 0)
        ]
        super().__init__("Surskit", 40, moves, "./TVPoke/Pokemon/imgs/Surskit.png")

class Masquerain(Bug):
    def __init__(self):
        moves = [
            Move("Gust", "FLYING", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Stun Spore", "GRASS", 0),
            Move("Air Slash", "FLYING", 75)
        ]
        super().__init__("Masquerain", 70, moves, "./TVPoke/Pokemon/imgs/Masquerain.png")

class Nincada(Bug):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Leech Life", "BUG", 80),
            Move("Sand Attack", "GROUND", 0)
        ]
        super().__init__("Nincada", 31, moves, "./TVPoke/Pokemon/imgs/Nincada.png")

class Ninjask(Bug):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("X-Scissor", "BUG", 95),
            Move("Swords Dance", "NORMAL", 0)
        ]
        super().__init__("Ninjask", 61, moves, "./TVPoke/Pokemon/imgs/Ninjask.png")

class Shedinja(Bug):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Shadow Claw", "GHOST", 70),
            Move("X-Scissor", "BUG", 95)
        ]
        super().__init__("Shedinja", 1, moves, "./TVPoke/Pokemon/imgs/Shedinja.png")

class Volbeat(Bug):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Confuse Ray", "GHOST", 0),
            Move("Quick Attack", "NORMAL", 40),
            Move("Moonlight", "NORMAL", 0)
        ]
        super().__init__("Volbeat", 65, moves, "./TVPoke/Pokemon/imgs/Volbeat.png")

class Illumise(Bug):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Sweet Scent", "NORMAL", 0),
            Move("Charm", "NORMAL", 0),
            Move("Moonlight", "NORMAL", 0)
        ]
        super().__init__("Illumise", 65, moves, "./TVPoke/Pokemon/imgs/Illumise.png")

class Pinsir(Bug):
    def __init__(self):
        moves = [
            Move("Vice Grip", "NORMAL", 55),
            Move("Focus Energy", "NORMAL", 0),
            Move("Bind", "NORMAL", 15),
            Move("Seismic Toss", "FIGHTING", 0)
        ]
        super().__init__("Pinsir", 65, moves, "./TVPoke/Pokemon/imgs/Pinsir.png")

class Heracross(Bug):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Leer", "NORMAL", 0),
            Move("Horn Attack", "NORMAL", 65),
            Move("Endure", "NORMAL", 0)
        ]
        super().__init__("Heracross", 80, moves, "./TVPoke/Pokemon/imgs/Heracross.png")

class Armaldo(Bug):
    def __init__(self):
        moves = [
            Move("Water Gun", "WATER", 40),
            Move("Harden", "NORMAL", 0),
            Move("Mud Sport", "GROUND", 0),
            Move("Ancient Power", "ROCK", 60)
        ]
        super().__init__("Armaldo", 75, moves, "./TVPoke/Pokemon/imgs/Armaldo.png")
