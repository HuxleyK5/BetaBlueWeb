from TVPoke.BaseClasses.PokeTypes import Fighting
from TVPoke.BaseClasses.Move import Move
from random import randint

class Machop(Fighting):
    def __init__(self):
        super().__init__("Machop", 70, [
            Move("Low Kick", "FIGHTING", 0),
            Move("Leer", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Karate Chop", "FIGHTING", 50)
        ], "./TVPoke/Pokemon/imgs/Machop.png")

class Machoke(Fighting):
    def __init__(self):
        super().__init__("Machoke", 80, [
            Move("Low Kick", "FIGHTING", 0),
            Move("Leer", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Seismic Toss", "FIGHTING", 0)
        ], "./TVPoke/Pokemon/imgs/Machoke.png")

class Machamp(Fighting):
    def __init__(self):
        super().__init__("Machamp", 90, [
            Move("Low Kick", "FIGHTING", 0),
            Move("Leer", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Dynamic Punch", "FIGHTING", 100)
        ], "./TVPoke/Pokemon/imgs/Machamp.png")

class Makuhita(Fighting):
    def __init__(self):
        super().__init__("Makuhita", 72, [
            Move("Tackle", "NORMAL", 40),
            Move("Focus Energy", "NORMAL", 0),
            Move("Sand Attack", "GROUND", 0),
            Move("Arm Thrust", "FIGHTING", 15)
        ], "./TVPoke/Pokemon/imgs/Makuhita.png")

class Hariyama(Fighting):
    def __init__(self):
        super().__init__("Hariyama", 144, [
            Move("Tackle", "NORMAL", 40),
            Move("Focus Energy", "NORMAL", 0),
            Move("Sand Attack", "GROUND", 0),
            Move("Heavy Slam", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Hariyama.png")

class Meditite(Fighting):
    def __init__(self):
        super().__init__("Meditite", 30, [
            Move("Bide", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Meditate", "PSYCHIC", 0),
            Move("Vital Throw", "FIGHTING", 70)
        ], "./TVPoke/Pokemon/imgs/Meditite.png")

class Medicham(Fighting):
    def __init__(self):
        super().__init__("Medicham", 60, [
            Move("Bide", "NORMAL", 0),
            Move("Focus Energy", "NORMAL", 0),
            Move("Meditate", "PSYCHIC", 0),
            Move("High Jump Kick", "FIGHTING", 100)
        ], "./TVPoke/Pokemon/imgs/Medicham.png")
