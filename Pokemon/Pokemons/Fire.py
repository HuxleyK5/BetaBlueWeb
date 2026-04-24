from TVPoke.BaseClasses.PokeTypes import Fire
from TVPoke.BaseClasses.Move import Move

class Torchic(Fire):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Ember", "FIRE", 40),
            Move("Peck", "FLYING", 35)
        ]
        super().__init__("Torchic", 45, moves, "./TVPoke/Pokemon/imgs/Torchic.png")


class Combusken(Fire):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Ember", "FIRE", 40),
            Move("Double Kick", "FIGHTING", 30)
        ]
        super().__init__("Combusken", 60, moves, "./TVPoke/Pokemon/imgs/Combusken.png")


class Blaziken(Fire):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Ember", "FIRE", 40),
            Move("Blaze Kick", "FIRE", 85)
        ]
        super().__init__("Blaziken", 80, moves, "./TVPoke/Pokemon/imgs/Blaziken.png")


class Numel(Fire):
    def __init__(self):
        moves = [
            Move("Growl", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Magnitude", "GROUND", 0)
        ]
        super().__init__("Numel", 60, moves, "./TVPoke/Pokemon/imgs/Numel.png")


class Camerupt(Fire):
    def __init__(self):
        moves = [
            Move("Growl", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Stone Edge", "ROCK", 100)
        ]
        super().__init__("Camerupt", 70, moves, "./TVPoke/Pokemon/imgs/Camerupt.png")


class Slugma(Fire):
    def __init__(self):
        moves = [
            Move("Smog", "POISON", 30),
            Move("Ember", "FIRE", 40),
            Move("Rock Throw", "ROCK", 50),
            Move("Harden", "NORMAL", 0)
        ]
        super().__init__("Slugma", 40, moves, "./TVPoke/Pokemon/imgs/Slugma.png")


class Magcargo(Fire):
    def __init__(self):
        moves = [
            Move("Smog", "POISON", 30),
            Move("Ember", "FIRE", 40),
            Move("Lava Plume", "FIRE", 80),
            Move("Stone Edge", "ROCK", 100)
        ]
        super().__init__("Magcargo", 60, moves, "./TVPoke/Pokemon/imgs/Magcargo.png")


class Torkoal(Fire):
    def __init__(self):
        moves = [
            Move("Ember", "FIRE", 40),
            Move("Smog", "POISON", 30),
            Move("Curse", "GHOST", 0),
            Move("Flamethrower", "FIRE", 90)
        ]
        super().__init__("Torkoal", 70, moves, "./TVPoke/Pokemon/imgs/Torkoal.png")


class Vulpix(Fire):
    def __init__(self):
        moves = [
            Move("Ember", "FIRE", 40),
            Move("Tail Whip", "NORMAL", 0),
            Move("Quick Attack", "NORMAL", 40),
            Move("Roar", "NORMAL", 0)
        ]
        super().__init__("Vulpix", 38, moves, "./TVPoke/Pokemon/imgs/Vulpix.png")


class Ninetales(Fire):
    def __init__(self):
        moves = [
            Move("Fire Spin", "FIRE", 35),
            Move("Confuse Ray", "GHOST", 0),
            Move("Safeguard", "NORMAL", 0),
            Move("Nasty Plot", "DARK", 0)
        ]
        super().__init__("Ninetales", 73, moves, "./TVPoke/Pokemon/imgs/Ninetales.png")