from TVPoke.BaseClasses.PokeTypes import Dark
from TVPoke.BaseClasses.Move import Move
from random import randint

class Poochyena(Dark):
    def __init__(self):
        moves = [
            Move("Bite", "DARK", 60),
            Move("Tackle", "NORMAL", 35),
            Move("Scary Face", "NORMAL", 0),
            Move("Swagger", "NORMAL", 0)
        ]
        super().__init__("Poochyena", 35, moves, "./TVPoke/Pokemon/imgs/Poochyena.png")

class Mightyena(Dark):
    def __init__(self):
        moves = [
            Move("Bite", "DARK", 60),
            Move("Tackle", "NORMAL", 35),
            Move("Swagger", "NORMAL", 0),
            Move("Roar", "NORMAL", 0)
        ]
        super().__init__("Mightyena", 70, moves, "./TVPoke/Pokemon/imgs/Mightyena.png")

class Absol(Dark):
    def __init__(self):
        moves = [
            Move("Razor Wind", "NORMAL", 80),
            Move("Bite", "DARK", 60),
            Move("Quick Attack", "NORMAL", 40),
            Move("Scratch", "NORMAL", 40)
        ]
        super().__init__("Absol", 65, moves, "./TVPoke/Pokemon/imgs/Absol.png")

class Sableye(Dark):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Fake Out", "NORMAL", 40),
            Move("Scratch", "NORMAL", 40),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Sableye", 50, moves, "./TVPoke/Pokemon/imgs/Sableye.png")
