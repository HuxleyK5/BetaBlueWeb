from TVPoke.BaseClasses.PokeTypes import Dragon
from TVPoke.BaseClasses.Move import Move
from random import randint

class Bagon(Dragon):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Bite", "DARK", 60),
            Move("Ember", "FIRE", 40),
            Move("Rage", "NORMAL", 20)
        ]
        super().__init__("Bagon", 45, moves, "./TVPoke/Pokemon/imgs/Bagon.png")

class Shelgon(Dragon):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Bite", "DARK", 60),
            Move("Ember", "FIRE", 40),
            Move("Rage", "NORMAL", 20)
        ]
        super().__init__("Shelgon", 65, moves, "./TVPoke/Pokemon/imgs/Shelgon.png")

class Salamence(Dragon):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Bite", "DARK", 60),
            Move("Ember", "FIRE", 40),
            Move("Rage", "NORMAL", 20)
        ]
        super().__init__("Salamence", 95, moves, "./TVPoke/Pokemon/imgs/Salamence.png")

class Latias(Dragon):
    def __init__(self):
        moves = [
            Move("DragonBreath", "DRAGON", 60),
            Move("Refresh", "NORMAL", 0),
            Move("Water Sport", "WATER", 0),
            Move("Safeguard", "NORMAL", 0)
        ]
        super().__init__("Latias", 80, moves, "./TVPoke/Pokemon/imgs/Latias.png")

class Latios(Dragon):
    def __init__(self):
        moves = [
            Move("DragonBreath", "DRAGON", 60),
            Move("Refresh", "NORMAL", 0),
            Move("Protect", "NORMAL", 0),
            Move("Safeguard", "NORMAL", 0)
        ]
        super().__init__("Latios", 80, moves, "./TVPoke/Pokemon/imgs/Latios.png")

class Rayquaza(Dragon):
    def __init__(self):
        moves = [
            Move("Dragon Claw", "DRAGON", 80),
            Move("AncientPower", "ROCK", 60),
            Move("Twister", "DRAGON", 40),
            Move("Dragon Dance", "DRAGON", 0)
        ]
        super().__init__("Rayquaza", 105, moves, "./TVPoke/Pokemon/imgs/Rayquaza.png")

class Altaria(Dragon):
    def __init__(self):
        moves = [
            Move("Peck", "FLYING", 35),
            Move("Astonish", "GHOST", 30),
            Move("Fury Attack", "NORMAL", 15),
            Move("Mist", "ICE", 0)
        ]
        super().__init__("Altaria", 75, moves, "./TVPoke/Pokemon/imgs/Altaria.png")
