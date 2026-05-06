from TVPoke.BaseClasses.PokeTypes import Ground
from TVPoke.BaseClasses.Move import Move
from random import randint

class Sandshrew(Ground):
    def __init__(self):
        moves = [
            Move("Slash", "NORMAL", 70),
            Move("Swift", "NORMAL", 60),
            Move("Scratch", "NORMAL", 40),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Sandshrew", 50, moves, "./TVPoke/Pokemon/imgs/Sandshrew.png")

class Sandslash(Ground):
    def __init__(self):
        moves = [
            Move("Slash", "NORMAL", 70),
            Move("Scratch", "NORMAL", 40),
            Move("Poison Sting", "POISON", 15),
            Move("Sand-Attack", "GROUND", 0)
        ]
        super().__init__("Sandslash", 75, moves, "./TVPoke/Pokemon/imgs/Sandslash.png")

class Trapinch(Ground):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Bite", "DARK", 60),
            Move("Sand Tomb", "GROUND", 15),
            Move("Sand-Attack", "GROUND", 0)
        ]
        super().__init__("Trapinch", 45, moves, "./TVPoke/Pokemon/imgs/Trapinch.png")

class Vibrava(Ground):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Bite", "DARK", 60),
            Move("Sand Tomb", "GROUND", 15),
            Move("Sand-Attack", "GROUND", 0)
        ]
        super().__init__("Vibrava", 50, moves, "./TVPoke/Pokemon/imgs/Vibrava.png")

class Flygon(Ground):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Bite", "DARK", 60),
            Move("Sand Tomb", "GROUND", 15),
            Move("Sand-Attack", "GROUND", 0)
        ]
        super().__init__("Flygon", 80, moves, "./TVPoke/Pokemon/imgs/Flygon.png")

class Baltoy(Ground):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Psybeam", "PSYCHIC", 65),
            Move("AncientPower", "ROCK", 60),
            Move("Rock Tomb", "ROCK", 50)
        ]
        super().__init__("Baltoy", 40, moves, "./TVPoke/Pokemon/imgs/Baltoy.png")

class Claydol(Ground):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Psybeam", "PSYCHIC", 65),
            Move("AncientPower", "ROCK", 60),
            Move("Rock Tomb", "ROCK", 50)
        ]
        super().__init__("Claydol", 60, moves, "./TVPoke/Pokemon/imgs/Claydol.png")

class Phanpy(Ground):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Tackle", "NORMAL", 35),
            Move("Flail", "NORMAL", 0),
            Move("Defense Curl", "NORMAL", 0)
        ]
        super().__init__("Phanpy", 90, moves, "./TVPoke/Pokemon/imgs/Phanpy.png")

class Donphan(Ground):
    def __init__(self):
        moves = [
            Move("Horn Attack", "NORMAL", 65),
            Move("Fury Attack", "NORMAL", 15),
            Move("Flail", "NORMAL", 0),
            Move("Defense Curl", "NORMAL", 0)
        ]
        super().__init__("Donphan", 90, moves, "./TVPoke/Pokemon/imgs/Donphan.png")

class Rhyhorn(Ground):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Horn Attack", "NORMAL", 65),
            Move("Rock Blast", "ROCK", 25),
            Move("Fury Attack", "NORMAL", 15)
        ]
        super().__init__("Rhyhorn", 80, moves, "./TVPoke/Pokemon/imgs/Rhyhorn.png")

class Rhydon(Ground):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Horn Attack", "NORMAL", 65),
            Move("Rock Blast", "ROCK", 25),
            Move("Fury Attack", "NORMAL", 15)
        ]
        super().__init__("Rhydon", 105, moves, "./TVPoke/Pokemon/imgs/Rhydon.png")

class Groudon(Ground):
    def __init__(self):
        moves = [
            Move("Slash", "NORMAL", 70),
            Move("AncientPower", "ROCK", 60),
            Move("Mud Shot", "GROUND", 55),
            Move("Bulk Up", "FIGHTING", 0)
        ]
        super().__init__("Groudon", 100, moves, "./TVPoke/Pokemon/imgs/Groudon.png")
