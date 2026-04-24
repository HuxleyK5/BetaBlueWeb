from TVPoke.BaseClasses.PokeTypes import Rock
from TVPoke.BaseClasses.Move import Move
from random import randint

class Geodude(Rock):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Defense Curl", "NORMAL", 0),
            Move("Rock Throw", "ROCK", 50),
            Move("Earthquake", "GROUND", 100)
        ]
        super().__init__("Geodude", 40, moves, "./TVPoke/Pokemon/imgs/Geodude.png")

class Graveler(Rock):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Defense Curl", "NORMAL", 0),
            Move("Rock Throw", "ROCK", 50),
            Move("Rock Slide", "ROCK", 75)
        ]
        super().__init__("Graveler", 55, moves, "./TVPoke/Pokemon/imgs/Graveler.png")

class Golem(Rock):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Defense Curl", "NORMAL", 0),
            Move("Rock Throw", "ROCK", 50),
            Move("Stone Edge", "ROCK", 100)
        ]
        super().__init__("Golem", 80, moves, "./TVPoke/Pokemon/imgs/Golem.png")

class Nosepass(Rock):
    def __init__(self):
        moves = [
            Move("Magnet Rise", "ELECTRIC", 0),
            Move("Gravity", "PSYCHIC", 0),
            Move("Spark", "ELECTRIC", 65),
            Move("Power Gem", "ROCK", 80)
        ]
        super().__init__("Nosepass", 30, moves, "./TVPoke/Pokemon/imgs/Nosepass.png")



class Lunatone(Rock):
    def __init__(self):
        super().__init__("Lunatone", 90, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Hypnosis", "PSYCHIC", 0),
            Move("Meteor Mash", "STEEL", 90),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Lunatone.png")

class Solrock(Rock):
    def __init__(self):
        super().__init__("Solrock", 90, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Sunny Day", "FIRE", 0),
            Move("Solar Beam", "GRASS", 120),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Solrock.png")

class Lileep(Rock):
    def __init__(self):
        super().__init__("Lileep", 66, [
            Move("Constrict", "NORMAL", 10),
            Move("Acid", "POISON", 40),
            Move("Ingrain", "GRASS", 0),
            Move("Ancient Power", "ROCK", 60)
        ], "./TVPoke/Pokemon/imgs/Lileep.png")

class Cradily(Rock):
    def __init__(self):
        super().__init__("Cradily", 86, [
            Move("Constrict", "NORMAL", 10),
            Move("Acid", "POISON", 40),
            Move("Ingrain", "GRASS", 0),
            Move("Power Whip", "GRASS", 120)
        ], "./TVPoke/Pokemon/imgs/Cradily.png")

class Anorith(Rock):
    def __init__(self):
        super().__init__("Anorith", 45, [
            Move("Scratch", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Mud Sport", "GROUND", 0),
            Move("Fury Cutter", "BUG", 20)
        ], "./TVPoke/Pokemon/imgs/Anorith.png")

class Regirock(Rock):
    def __init__(self):
        super().__init__("Regirock", 80, [
            Move("Curse", "GHOST", 0),
            Move("Superpower", "FIGHTING", 120),
            Move("Stone Edge", "ROCK", 100),
            Move("Explosion", "NORMAL", 250)
        ], "./TVPoke/Pokemon/imgs/Regirock.png")

