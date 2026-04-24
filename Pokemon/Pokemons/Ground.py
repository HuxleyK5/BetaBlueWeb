from TVPoke.BaseClasses.PokeTypes import Ground
from TVPoke.BaseClasses.Move import Move
from random import randint



class Sandshrew(Ground):
    def __init__(self):
        super().__init__("Sandshrew", 50, [
            Move("Scratch", "NORMAL", 40),
            Move("Sand Attack", "GROUND", 0),
            Move("Defense Curl", "NORMAL", 0),
            Move("Slash", "NORMAL", 70)
        ], "./TVPoke/Pokemon/imgs/Sandshrew.png")

class Sandslash(Ground):
    def __init__(self):
        super().__init__("Sandslash", 75, [
            Move("Scratch", "NORMAL", 40),
            Move("Sand Attack", "GROUND", 0),
            Move("Sand Tomb", "GROUND", 35),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Sandslash.png")

class Trapinch(Ground):
    def __init__(self):
        super().__init__("Trapinch", 45, [
            Move("Bite", "DARK", 60),
            Move("Sand Attack", "GROUND", 0),
            Move("Foresight", "NORMAL", 0),
            Move("Sand Tomb", "GROUND", 35)
        ], "./TVPoke/Pokemon/imgs/Trapinch.png")

class Vibrava(Ground):
    def __init__(self):
        super().__init__("Vibrava", 50, [
            Move("Bite", "DARK", 60),
            Move("Supersonic", "NORMAL", 0),
            Move("Dragon Breath", "DRAGON", 60),
            Move("Sand Tomb", "GROUND", 35)
        ], "./TVPoke/Pokemon/imgs/Vibrava.png")

class Flygon(Ground):
    def __init__(self):
        super().__init__("Flygon", 80, [
            Move("Dragon Breath", "DRAGON", 60),
            Move("Sand Attack", "GROUND", 0),
            Move("Crunch", "DARK", 80),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Flygon.png")

class Baltoy(Ground):
    def __init__(self):
        super().__init__("Baltoy", 40, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Mud Slap", "GROUND", 20),
            Move("Harden", "NORMAL", 0),
            Move("Ancient Power", "ROCK", 60)
        ], "./TVPoke/Pokemon/imgs/Baltoy.png")

class Claydol(Ground):
    def __init__(self):
        super().__init__("Claydol", 60, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Mud Slap", "GROUND", 20),
            Move("Harden", "NORMAL", 0),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Claydol.png")

class Phanpy(Ground):
    def __init__(self):
        super().__init__("Phanpy", 90, [
            Move("Growl", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Mud Slap", "GROUND", 20),
            Move("Rollout", "ROCK", 30)
        ], "./TVPoke/Pokemon/imgs/Phanpy.png")

class Donphan(Ground):
    def __init__(self):
        super().__init__("Donphan", 90, [
            Move("Growl", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Mud Slap", "GROUND", 20),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Donphan.png")

class Rhyhorn(Ground):
    def __init__(self):
        super().__init__("Rhyhorn", 80, [
            Move("Fury Attack", "NORMAL", 15),
            Move("Scary Face", "NORMAL", 0),
            Move("Stomp", "NORMAL", 65),
            Move("Horn Drill", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Rhyhorn.png")

class Rhydon(Ground):
    def __init__(self):
        super().__init__("Rhydon", 105, [
            Move("Fury Attack", "NORMAL", 15),
            Move("Scary Face", "NORMAL", 0),
            Move("Stomp", "NORMAL", 65),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Rhydon.png")

class Groudon(Ground):
    def __init__(self):
        super().__init__("Groudon", 100, [
            Move("Mud Shot", "GROUND", 55),
            Move("Scary Face", "NORMAL", 0),
            Move("Stomp", "NORMAL", 65),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Groudon.png")
