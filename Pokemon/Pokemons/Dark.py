from TVPoke.BaseClasses.PokeTypes import Dark
from TVPoke.BaseClasses.Move import Move
from random import randint

class Poochyena(Dark):
    def __init__(self):
        super().__init__("Poochyena", 35, [
            Move("Tackle", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Sand Attack", "GROUND", 0),
            Move("Bite", "DARK", 60)
        ], "./TVPoke/Pokemon/imgs/Poochyena.png")

class Mightyena(Dark):
    def __init__(self):
        super().__init__("Mightyena", 70, [
            Move("Tackle", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Sand Attack", "GROUND", 0),
            Move("Crunch", "DARK", 80)
        ], "./TVPoke/Pokemon/imgs/Mightyena.png")

class Absol(Dark):
    def __init__(self):
        super().__init__("Absol", 65, [
            Move("Scratch", "NORMAL", 40),
            Move("Leer", "NORMAL", 0),
            Move("Taunt", "DARK", 0),
            Move("Psycho Cut", "PSYCHIC", 70)
        ], "./TVPoke/Pokemon/imgs/Absol.png")

class Sableye(Dark):
    def __init__(self):
        super().__init__("Sableye", 50, [
            Move("Scratch", "NORMAL", 40),
            Move("Leer", "NORMAL", 0),
            Move("Night Shade", "GHOST", 0),
            Move("Shadow Claw", "GHOST", 70)
        ], "./TVPoke/Pokemon/imgs/Sableye.png")

