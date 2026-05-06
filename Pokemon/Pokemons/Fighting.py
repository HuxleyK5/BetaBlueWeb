from TVPoke.BaseClasses.PokeTypes import Fighting
from TVPoke.BaseClasses.Move import Move
from random import randint

class Machop(Fighting):
    def __init__(self):
        moves = [
            Move("Revenge", "FIGHTING", 60),
            Move("Karate Chop", "FIGHTING", 50),
            Move("Foresight", "NORMAL", 0),
            Move("Seismic Toss", "FIGHTING", 0)
        ]
        super().__init__("Machop", 70, moves, "./TVPoke/Pokemon/imgs/Machop.png")

class Machoke(Fighting):
    def __init__(self):
        moves = [
            Move("Revenge", "FIGHTING", 60),
            Move("Karate Chop", "FIGHTING", 50),
            Move("Foresight", "NORMAL", 0),
            Move("Seismic Toss", "FIGHTING", 0)
        ]
        super().__init__("Machoke", 80, moves, "./TVPoke/Pokemon/imgs/Machoke.png")

class Machamp(Fighting):
    def __init__(self):
        moves = [
            Move("Revenge", "FIGHTING", 60),
            Move("Karate Chop", "FIGHTING", 50),
            Move("Foresight", "NORMAL", 0),
            Move("Seismic Toss", "FIGHTING", 0)
        ]
        super().__init__("Machamp", 90, moves, "./TVPoke/Pokemon/imgs/Machamp.png")

class Makuhita(Fighting):
    def __init__(self):
        moves = [
            Move("Vital Throw", "FIGHTING", 70),
            Move("Fake Out", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Knock Off", "DARK", 20)
        ]
        super().__init__("Makuhita", 72, moves, "./TVPoke/Pokemon/imgs/Makuhita.png")

class Hariyama(Fighting):
    def __init__(self):
        moves = [
            Move("Vital Throw", "FIGHTING", 70),
            Move("Fake Out", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Knock Off", "DARK", 20)
        ]
        super().__init__("Hariyama", 144, moves, "./TVPoke/Pokemon/imgs/Hariyama.png")

class Meditite(Fighting):
    def __init__(self):
        moves = [
            Move("Hidden Power", "NORMAL", 60),
            Move("Confusion", "PSYCHIC", 50),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Mind Reader", "NORMAL", 0)
        ]
        super().__init__("Meditite", 30, moves, "./TVPoke/Pokemon/imgs/Meditite.png")

class Medicham(Fighting):
    def __init__(self):
        moves = [
            Move("ThunderPunch", "ELECTRIC", 75),
            Move("Ice Punch", "ICE", 75),
            Move("Fire Punch", "FIRE", 75),
            Move("Hidden Power", "NORMAL", 60)
        ]
        super().__init__("Medicham", 60, moves, "./TVPoke/Pokemon/imgs/Medicham.png")
