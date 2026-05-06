from TVPoke.BaseClasses.PokeTypes import Psychic
from TVPoke.BaseClasses.Move import Move
from random import randint

class Ralts(Psychic):
    def __init__(self):
        moves = [
            Move("Psychic", "PSYCHIC", 90),
            Move("Confusion", "PSYCHIC", 50),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Teleport", "PSYCHIC", 0)
        ]
        super().__init__("Ralts", 28, moves, "./TVPoke/Pokemon/imgs/Ralts.png")

class Kirlia(Psychic):
    def __init__(self):
        moves = [
            Move("Psychic", "PSYCHIC", 90),
            Move("Confusion", "PSYCHIC", 50),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Teleport", "PSYCHIC", 0)
        ]
        super().__init__("Kirlia", 38, moves, "./TVPoke/Pokemon/imgs/Kirlia.png")

class Gardevoir(Psychic):
    def __init__(self):
        moves = [
            Move("Psychic", "PSYCHIC", 90),
            Move("Confusion", "PSYCHIC", 50),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Teleport", "PSYCHIC", 0)
        ]
        super().__init__("Gardevoir", 68, moves, "./TVPoke/Pokemon/imgs/Gardevoir.png")

class Abra(Psychic):
    def __init__(self):
        moves = [
            Move("Teleport", "PSYCHIC", 0)
        ]
        super().__init__("Abra", 25, moves, "./TVPoke/Pokemon/imgs/Abra.png")

class Kadabra(Psychic):
    def __init__(self):
        moves = [
            Move("Future Sight", "PSYCHIC", 80),
            Move("Psybeam", "PSYCHIC", 65),
            Move("Confusion", "PSYCHIC", 50),
            Move("Recover", "NORMAL", 0)
        ]
        super().__init__("Kadabra", 40, moves, "./TVPoke/Pokemon/imgs/Kadabra.png")

class Alakazam(Psychic):
    def __init__(self):
        moves = [
            Move("Future Sight", "PSYCHIC", 80),
            Move("Psybeam", "PSYCHIC", 65),
            Move("Confusion", "PSYCHIC", 50),
            Move("Recover", "NORMAL", 0)
        ]
        super().__init__("Alakazam", 55, moves, "./TVPoke/Pokemon/imgs/Alakazam.png")

class Spoink(Psychic):
    def __init__(self):
        moves = [
            Move("Psybeam", "PSYCHIC", 65),
            Move("Magic Coat", "PSYCHIC", 0),
            Move("Confuse Ray", "GHOST", 0),
            Move("Psych Up", "NORMAL", 0)
        ]
        super().__init__("Spoink", 60, moves, "./TVPoke/Pokemon/imgs/Spoink.png")

class Grumpig(Psychic):
    def __init__(self):
        moves = [
            Move("Psybeam", "PSYCHIC", 65),
            Move("Magic Coat", "PSYCHIC", 0),
            Move("Confuse Ray", "GHOST", 0),
            Move("Psych Up", "NORMAL", 0)
        ]
        super().__init__("Grumpig", 80, moves, "./TVPoke/Pokemon/imgs/Grumpig.png")

class Natu(Psychic):
    def __init__(self):
        moves = [
            Move("Future Sight", "PSYCHIC", 80),
            Move("Peck", "FLYING", 35),
            Move("Wish", "NORMAL", 0),
            Move("Teleport", "PSYCHIC", 0)
        ]
        super().__init__("Natu", 40, moves, "./TVPoke/Pokemon/imgs/Natu.png")

class Xatu(Psychic):
    def __init__(self):
        moves = [
            Move("Peck", "FLYING", 35),
            Move("Teleport", "PSYCHIC", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Leer", "NORMAL", 0)
        ]
        super().__init__("Xatu", 65, moves, "./TVPoke/Pokemon/imgs/Xatu.png")

class Wynaut(Psychic):
    def __init__(self):
        moves = [
            Move("Safeguard", "NORMAL", 0),
            Move("Mirror Coat", "PSYCHIC", 0),
            Move("Destiny Bond", "GHOST", 0),
            Move("Counter", "FIGHTING", 0)
        ]
        super().__init__("Wynaut", 95, moves, "./TVPoke/Pokemon/imgs/Wynaut.png")

class Wobbuffet(Psychic):
    def __init__(self):
        moves = [
            Move("Safeguard", "NORMAL", 0),
            Move("Mirror Coat", "PSYCHIC", 0),
            Move("Destiny Bond", "GHOST", 0),
            Move("Counter", "FIGHTING", 0)
        ]
        super().__init__("Wobbuffet", 190, moves, "./TVPoke/Pokemon/imgs/Wobbuffet.png")

class Girafarig(Psychic):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Confusion", "PSYCHIC", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Girafarig", 70, moves, "./TVPoke/Pokemon/imgs/Girafarig.png")

class Chimecho(Psychic):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Uproar", "NORMAL", 50),
            Move("Confusion", "PSYCHIC", 50),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Chimecho", 75, moves, "./TVPoke/Pokemon/imgs/Chimecho.png")

class Deoxys(Psychic):
    def __init__(self):
        moves = [
            Move("Psychic", "PSYCHIC", 90),
            Move("Pursuit", "DARK", 40),
            Move("Knock Off", "DARK", 20),
            Move("Wrap", "NORMAL", 15)
        ]
        super().__init__("Deoxys", 50, moves, "./TVPoke/Pokemon/imgs/Deoxys.png")
