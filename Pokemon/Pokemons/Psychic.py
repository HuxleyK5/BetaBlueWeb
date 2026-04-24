from TVPoke.BaseClasses.PokeTypes import Psychic
from TVPoke.BaseClasses.Move import Move
from random import randint

class Ralts(Psychic):
    def __init__(self):
        super().__init__("Ralts", 28, [
            Move("Growl", "NORMAL", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Double Team", "NORMAL", 0),
            Move("Teleport", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Ralts.png")

class Kirlia(Psychic):
    def __init__(self):
        super().__init__("Kirlia", 38, [
            Move("Growl", "NORMAL", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Kirlia.png")

class Gardevoir(Psychic):
    def __init__(self):
        super().__init__("Gardevoir", 68, [
            Move("Growl", "NORMAL", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Double Team", "NORMAL", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Gardevoir.png")

class Abra(Psychic):
    def __init__(self):
        super().__init__("Abra", 25, [
            Move("Teleport", "PSYCHIC", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Mirror Coat", "PSYCHIC", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Abra.png")

class Kadabra(Psychic):
    def __init__(self):
        super().__init__("Kadabra", 40, [
            Move("Teleport", "PSYCHIC", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Disable", "NORMAL", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Kadabra.png")

class Alakazam(Psychic):
    def __init__(self):
        super().__init__("Alakazam", 55, [
            Move("Teleport", "PSYCHIC", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Focus Blast", "FIGHTING", 120),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Alakazam.png")

class Spoink(Psychic):
    def __init__(self):
        super().__init__("Spoink", 60, [
            Move("Psywave", "PSYCHIC", 0),
            Move("Odor Sleuth", "NORMAL", 0),
            Move("Bounce", "NORMAL", 85),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Spoink.png")

class Grumpig(Psychic):
    def __init__(self):
        super().__init__("Grumpig", 80, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Magic Coat", "PSYCHIC", 0),
            Move("Psybeam", "PSYCHIC", 65),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Grumpig.png")

class Natu(Psychic):
    def __init__(self):
        super().__init__("Natu", 40, [
            Move("Peck", "FLYING", 35),
            Move("Leer", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Teleport", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Natu.png")

class Xatu(Psychic):
    def __init__(self):
        super().__init__("Xatu", 65, [
            Move("Peck", "FLYING", 35),
            Move("Leer", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Xatu.png")

class Wynaut(Psychic):
    def __init__(self):
        super().__init__("Wynaut", 95, [
            Move("Pound", "NORMAL", 40),
            Move("Encore", "NORMAL", 0),
            Move("Copycat", "NORMAL", 0),
            Move("Mirror Coat", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Wynaut.png")

class Wobbuffet(Psychic):
    def __init__(self):
        super().__init__("Wobbuffet", 190, [
            Move("Pound", "NORMAL", 40),
            Move("Encore", "NORMAL", 0),
            Move("Copycat", "NORMAL", 0),
            Move("Mirror Coat", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Wobbuffet.png")

class Girafarig(Psychic):
    def __init__(self):
        super().__init__("Girafarig", 70, [
            Move("Tackle", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Astonish", "GHOST", 30),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Girafarig.png")

class Chimecho(Psychic):
    def __init__(self):
        super().__init__("Chimecho", 75, [
            Move("Wrap", "NORMAL", 15),
            Move("Growl", "NORMAL", 0),
            Move("Confusion", "PSYCHIC", 50),
            Move("Psywave", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Chimecho.png")



class Deoxys(Psychic):
    def __init__(self):
        super().__init__("Deoxys", 50, [
            Move("Wrap", "NORMAL", 15),
            Move("Psywave", "PSYCHIC", 0),
            Move("Astonish", "GHOST", 30),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Deoxys.png")

