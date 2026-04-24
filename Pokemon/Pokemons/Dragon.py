from TVPoke.BaseClasses.PokeTypes import Dragon
from TVPoke.BaseClasses.Move import Move
from random import randint

class Bagon(Dragon):
    def __init__(self):
        super().__init__("Bagon", 45, [
            Move("Rage", "NORMAL", 20),
            Move("Leer", "NORMAL", 0),
            Move("Bite", "DARK", 60),
            Move("Dragon Claw", "DRAGON", 80)
        ], "./TVPoke/Pokemon/imgs/Bagon.png")

class Shelgon(Dragon):
    def __init__(self):
        super().__init__("Shelgon", 65, [
            Move("Headbutt", "NORMAL", 70),
            Move("Leer", "NORMAL", 0),
            Move("Protect", "NORMAL", 0),
            Move("Dragon Claw", "DRAGON", 80)
        ], "./TVPoke/Pokemon/imgs/Shelgon.png")

class Salamence(Dragon):
    def __init__(self):
        super().__init__("Salamence", 95, [
            Move("Fly", "FLYING", 90),
            Move("Leer", "NORMAL", 0),
            Move("Crunch", "DARK", 80),
            Move("Dragon Dance", "DRAGON", 0)
        ], "./TVPoke/Pokemon/imgs/Salamence.png")

class Latias(Dragon):
    def __init__(self):
        super().__init__("Latias", 80, [
            Move("Dragon Breath", "DRAGON", 60),
            Move("Recover", "NORMAL", 0),
            Move("Light Screen", "PSYCHIC", 0),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Latias.png")

class Latios(Dragon):
    def __init__(self):
        super().__init__("Latios", 80, [
            Move("Dragon Breath", "DRAGON", 60),
            Move("Recover", "NORMAL", 0),
            Move("Calm Mind", "PSYCHIC", 0),
            Move("Luster Purge", "PSYCHIC", 70)
        ], "./TVPoke/Pokemon/imgs/Latios.png")

class Rayquaza(Dragon):
    def __init__(self):
        super().__init__("Rayquaza", 105, [
            Move("Twister", "DRAGON", 40),
            Move("Scary Face", "NORMAL", 0),
            Move("Dragon Dance", "DRAGON", 0),
            Move("Outrage", "DRAGON", 120)
        ], "./TVPoke/Pokemon/imgs/Rayquaza.png")



class Altaria(Dragon):
    def __init__(self):
        super().__init__("Altaria", 75, [
            Move("Peck", "FLYING", 35),
            Move("Growl", "NORMAL", 0),
            Move("Dragon Breath", "DRAGON", 60),
            Move("Dragon Claw", "DRAGON", 80)
        ], "./TVPoke/Pokemon/imgs/Altaria.png")

