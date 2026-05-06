from TVPoke.BaseClasses.PokeTypes import Steel
from TVPoke.BaseClasses.Move import Move
from random import randint

class Mawile(Steel):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Bite", "DARK", 60),
            Move("ViceGrip", "NORMAL", 55),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Mawile", 50, moves, "./TVPoke/Pokemon/imgs/Mawile.png")

class Aron(Steel):
    def __init__(self):
        moves = [
            Move("Iron Tail", "STEEL", 100),
            Move("Take Down", "NORMAL", 90),
            Move("Headbutt", "NORMAL", 70),
            Move("Metal Claw", "STEEL", 50)
        ]
        super().__init__("Aron", 50, moves, "./TVPoke/Pokemon/imgs/Aron.png")

class Lairon(Steel):
    def __init__(self):
        moves = [
            Move("Iron Tail", "STEEL", 100),
            Move("Take Down", "NORMAL", 90),
            Move("Headbutt", "NORMAL", 70),
            Move("Metal Claw", "STEEL", 50)
        ]
        super().__init__("Lairon", 60, moves, "./TVPoke/Pokemon/imgs/Lairon.png")

class Aggron(Steel):
    def __init__(self):
        moves = [
            Move("Iron Tail", "STEEL", 100),
            Move("Take Down", "NORMAL", 90),
            Move("Headbutt", "NORMAL", 70),
            Move("Metal Claw", "STEEL", 50)
        ]
        super().__init__("Aggron", 70, moves, "./TVPoke/Pokemon/imgs/Aggron.png")

class Beldum(Steel):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90)
        ]
        super().__init__("Beldum", 40, moves, "./TVPoke/Pokemon/imgs/Beldum.png")

class Metang(Steel):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Metal Claw", "STEEL", 50),
            Move("Confusion", "PSYCHIC", 50),
            Move("Scary Face", "NORMAL", 0)
        ]
        super().__init__("Metang", 60, moves, "./TVPoke/Pokemon/imgs/Metang.png")

class Metagross(Steel):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Metal Claw", "STEEL", 50),
            Move("Confusion", "PSYCHIC", 50),
            Move("Scary Face", "NORMAL", 0)
        ]
        super().__init__("Metagross", 80, moves, "./TVPoke/Pokemon/imgs/Metagross.png")

class Registeel(Steel):
    def __init__(self):
        moves = [
            Move("Explosion", "NORMAL", 250),
            Move("Superpower", "FIGHTING", 120),
            Move("Metal Claw", "STEEL", 50),
            Move("Curse", "???", 0)
        ]
        super().__init__("Registeel", 80, moves, "./TVPoke/Pokemon/imgs/Registeel.png")

class Skarmory(Steel):
    def __init__(self):
        moves = [
            Move("Swift", "NORMAL", 60),
            Move("Air Cutter", "FLYING", 55),
            Move("Peck", "FLYING", 35),
            Move("Fury Attack", "NORMAL", 15)
        ]
        super().__init__("Skarmory", 65, moves, "./TVPoke/Pokemon/imgs/Skarmory.png")

class Jirachi(Steel):
    def __init__(self):
        moves = [
            Move("Psychic", "PSYCHIC", 90),
            Move("Swift", "NORMAL", 60),
            Move("Confusion", "PSYCHIC", 50),
            Move("Refresh", "NORMAL", 0)
        ]
        super().__init__("Jirachi", 100, moves, "./TVPoke/Pokemon/imgs/Jirachi.png")
