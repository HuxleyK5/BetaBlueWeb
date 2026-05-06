from TVPoke.BaseClasses.PokeTypes import Fire
from TVPoke.BaseClasses.Move import Move

class Torchic(Fire):
    def __init__(self):
        moves = [
            Move("Quick Attack", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Scratch", "NORMAL", 40),
            Move("Peck", "FLYING", 35)
        ]
        super().__init__("Torchic", 45, moves, "./TVPoke/Pokemon/imgs/Torchic.png")

class Combusken(Fire):
    def __init__(self):
        moves = [
            Move("Scratch", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Peck", "FLYING", 35),
            Move("Double Kick", "FIGHTING", 30)
        ]
        super().__init__("Combusken", 60, moves, "./TVPoke/Pokemon/imgs/Combusken.png")

class Blaziken(Fire):
    def __init__(self):
        moves = [
            Move("Fire Punch", "FIRE", 75),
            Move("Scratch", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Peck", "FLYING", 35)
        ]
        super().__init__("Blaziken", 80, moves, "./TVPoke/Pokemon/imgs/Blaziken.png")

class Numel(Fire):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Ember", "FIRE", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Focus Energy", "NORMAL", 0)
        ]
        super().__init__("Numel", 60, moves, "./TVPoke/Pokemon/imgs/Numel.png")

class Camerupt(Fire):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Ember", "FIRE", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Focus Energy", "NORMAL", 0)
        ]
        super().__init__("Camerupt", 70, moves, "./TVPoke/Pokemon/imgs/Camerupt.png")

class Slugma(Fire):
    def __init__(self):
        moves = [
            Move("Rock Throw", "ROCK", 50),
            Move("Ember", "FIRE", 40),
            Move("Smog", "POISON", 20),
            Move("Amnesia", "PSYCHIC", 0)
        ]
        super().__init__("Slugma", 40, moves, "./TVPoke/Pokemon/imgs/Slugma.png")

class Magcargo(Fire):
    def __init__(self):
        moves = [
            Move("Rock Throw", "ROCK", 50),
            Move("Ember", "FIRE", 40),
            Move("Smog", "POISON", 20),
            Move("Amnesia", "PSYCHIC", 0)
        ]
        super().__init__("Magcargo", 60, moves, "./TVPoke/Pokemon/imgs/Magcargo.png")

class Torkoal(Fire):
    def __init__(self):
        moves = [
            Move("Flamethrower", "FIRE", 95),
            Move("Body Slam", "NORMAL", 85),
            Move("Ember", "FIRE", 40),
            Move("Smog", "POISON", 20)
        ]
        super().__init__("Torkoal", 70, moves, "./TVPoke/Pokemon/imgs/Torkoal.png")

class Vulpix(Fire):
    def __init__(self):
        moves = [
            Move("Flamethrower", "FIRE", 95),
            Move("Quick Attack", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Imprison", "PSYCHIC", 0)
        ]
        super().__init__("Vulpix", 38, moves, "./TVPoke/Pokemon/imgs/Vulpix.png")

class Ninetales(Fire):
    def __init__(self):
        moves = [
            Move("Quick Attack", "NORMAL", 40),
            Move("Ember", "FIRE", 40),
            Move("Safeguard", "NORMAL", 0),
            Move("Confuse Ray", "GHOST", 0)
        ]
        super().__init__("Ninetales", 73, moves, "./TVPoke/Pokemon/imgs/Ninetales.png")
