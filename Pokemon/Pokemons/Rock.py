from TVPoke.BaseClasses.PokeTypes import Rock
from TVPoke.BaseClasses.Move import Move
from random import randint

class Geodude(Rock):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Rock Throw", "ROCK", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Geodude", 40, moves, "./TVPoke/Pokemon/imgs/Geodude.png")

class Graveler(Rock):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Rock Throw", "ROCK", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Graveler", 55, moves, "./TVPoke/Pokemon/imgs/Graveler.png")

class Golem(Rock):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Rock Throw", "ROCK", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Golem", 80, moves, "./TVPoke/Pokemon/imgs/Golem.png")

class Nosepass(Rock):
    def __init__(self):
        moves = [
            Move("Rock Slide", "ROCK", 75),
            Move("Rock Throw", "ROCK", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Thunder Wave", "ELECTRIC", 0)
        ]
        super().__init__("Nosepass", 30, moves, "./TVPoke/Pokemon/imgs/Nosepass.png")

class Lunatone(Rock):
    def __init__(self):
        moves = [
            Move("Rock Throw", "ROCK", 50),
            Move("Confusion", "PSYCHIC", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Psywave", "PSYCHIC", 0)
        ]
        super().__init__("Lunatone", 90, moves, "./TVPoke/Pokemon/imgs/Lunatone.png")

class Solrock(Rock):
    def __init__(self):
        moves = [
            Move("Rock Throw", "ROCK", 50),
            Move("Confusion", "PSYCHIC", 50),
            Move("Tackle", "NORMAL", 35),
            Move("Fire Spin", "FIRE", 15)
        ]
        super().__init__("Solrock", 90, moves, "./TVPoke/Pokemon/imgs/Solrock.png")

class Lileep(Rock):
    def __init__(self):
        moves = [
            Move("Acid", "POISON", 40),
            Move("Astonish", "GHOST", 30),
            Move("Constrict", "NORMAL", 10),
            Move("Confuse Ray", "GHOST", 0)
        ]
        super().__init__("Lileep", 66, moves, "./TVPoke/Pokemon/imgs/Lileep.png")

class Cradily(Rock):
    def __init__(self):
        moves = [
            Move("Acid", "POISON", 40),
            Move("Astonish", "GHOST", 30),
            Move("Constrict", "NORMAL", 10),
            Move("Confuse Ray", "GHOST", 0)
        ]
        super().__init__("Cradily", 86, moves, "./TVPoke/Pokemon/imgs/Cradily.png")

class Anorith(Rock):
    def __init__(self):
        moves = [
            Move("Metal Claw", "STEEL", 50),
            Move("Water Gun", "WATER", 40),
            Move("Scratch", "NORMAL", 40),
            Move("Mud Sport", "GROUND", 0)
        ]
        super().__init__("Anorith", 45, moves, "./TVPoke/Pokemon/imgs/Anorith.png")

class Regirock(Rock):
    def __init__(self):
        moves = [
            Move("Explosion", "NORMAL", 250),
            Move("Superpower", "FIGHTING", 120),
            Move("Rock Throw", "ROCK", 50),
            Move("Curse", "???", 0)
        ]
        super().__init__("Regirock", 80, moves, "./TVPoke/Pokemon/imgs/Regirock.png")
