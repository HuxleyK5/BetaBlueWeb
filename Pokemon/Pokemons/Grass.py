from TVPoke.BaseClasses.PokeTypes import Grass
from TVPoke.BaseClasses.Move import Move

class Treecko(Grass):
    def __init__(self):
        moves = [
            Move("Mega Drain", "GRASS", 40),
            Move("Pursuit", "DARK", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Pound", "NORMAL", 40)
        ]
        super().__init__("Treecko", 40, moves, "./TVPoke/Pokemon/imgs/Treecko.png")

class Grovyle(Grass):
    def __init__(self):
        moves = [
            Move("Leaf Blade", "GRASS", 70),
            Move("Pursuit", "DARK", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Pound", "NORMAL", 40)
        ]
        super().__init__("Grovyle", 50, moves, "./TVPoke/Pokemon/imgs/Grovyle.png")

class Sceptile(Grass):
    def __init__(self):
        moves = [
            Move("Leaf Blade", "GRASS", 70),
            Move("Pursuit", "DARK", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Pound", "NORMAL", 40)
        ]
        super().__init__("Sceptile", 70, moves, "./TVPoke/Pokemon/imgs/Sceptile.png")

class Lotad(Grass):
    def __init__(self):
        moves = [
            Move("Astonish", "GHOST", 30),
            Move("Absorb", "GRASS", 20),
            Move("Mist", "ICE", 0),
            Move("Nature Power", "NORMAL", 0)
        ]
        super().__init__("Lotad", 40, moves, "./TVPoke/Pokemon/imgs/Lotad.png")

class Lombre(Grass):
    def __init__(self):
        moves = [
            Move("Fake Out", "NORMAL", 40),
            Move("Astonish", "GHOST", 30),
            Move("Absorb", "GRASS", 20),
            Move("Fury Swipes", "NORMAL", 18)
        ]
        super().__init__("Lombre", 60, moves, "./TVPoke/Pokemon/imgs/Lombre.png")

class Ludicolo(Grass):
    def __init__(self):
        moves = [
            Move("Astonish", "GHOST", 30),
            Move("Absorb", "GRASS", 20),
            Move("Nature Power", "NORMAL", 0),
            Move("Growl", "NORMAL", 0)
        ]
        super().__init__("Ludicolo", 80, moves, "./TVPoke/Pokemon/imgs/Ludicolo.png")

class Seedot(Grass):
    def __init__(self):
        moves = [
            Move("Synthesis", "GRASS", 0),
            Move("Nature Power", "NORMAL", 0),
            Move("Growth", "NORMAL", 0),
            Move("Harden", "NORMAL", 0)
        ]
        super().__init__("Seedot", 40, moves, "./TVPoke/Pokemon/imgs/Seedot.png")

class Nuzleaf(Grass):
    def __init__(self):
        moves = [
            Move("Fake Out", "NORMAL", 40),
            Move("Pound", "NORMAL", 40),
            Move("Torment", "DARK", 0),
            Move("Nature Power", "NORMAL", 0)
        ]
        super().__init__("Nuzleaf", 70, moves, "./TVPoke/Pokemon/imgs/Nuzleaf.png")

class Shiftry(Grass):
    def __init__(self):
        moves = [
            Move("Pound", "NORMAL", 40),
            Move("Nature Power", "NORMAL", 0),
            Move("Harden", "NORMAL", 0),
            Move("Growth", "NORMAL", 0)
        ]
        super().__init__("Shiftry", 90, moves, "./TVPoke/Pokemon/imgs/Shiftry.png")

class Shroomish(Grass):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Mega Drain", "GRASS", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Absorb", "GRASS", 20)
        ]
        super().__init__("Shroomish", 60, moves, "./TVPoke/Pokemon/imgs/Shroomish.png")

class Breloom(Grass):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Mach Punch", "FIGHTING", 40),
            Move("Mega Drain", "GRASS", 40),
            Move("Tackle", "NORMAL", 35)
        ]
        super().__init__("Breloom", 60, moves, "./TVPoke/Pokemon/imgs/Breloom.png")

class Oddish(Grass):
    def __init__(self):
        moves = [
            Move("Acid", "POISON", 40),
            Move("Absorb", "GRASS", 20),
            Move("Sleep Powder", "GRASS", 0),
            Move("Stun Spore", "GRASS", 0)
        ]
        super().__init__("Oddish", 45, moves, "./TVPoke/Pokemon/imgs/Oddish.png")

class Gloom(Grass):
    def __init__(self):
        moves = [
            Move("Acid", "POISON", 40),
            Move("Absorb", "GRASS", 20),
            Move("Sleep Powder", "GRASS", 0),
            Move("Stun Spore", "GRASS", 0)
        ]
        super().__init__("Gloom", 60, moves, "./TVPoke/Pokemon/imgs/Gloom.png")

class Vileplume(Grass):
    def __init__(self):
        moves = [
            Move("Mega Drain", "GRASS", 40),
            Move("Absorb", "GRASS", 20),
            Move("Stun Spore", "GRASS", 0),
            Move("Aromatherapy", "GRASS", 0)
        ]
        super().__init__("Vileplume", 75, moves, "./TVPoke/Pokemon/imgs/Vileplume.png")

class Bellossom(Grass):
    def __init__(self):
        moves = [
            Move("Magical Leaf", "GRASS", 60),
            Move("Absorb", "GRASS", 20),
            Move("Sweet Scent", "NORMAL", 0),
            Move("Stun Spore", "GRASS", 0)
        ]
        super().__init__("Bellossom", 75, moves, "./TVPoke/Pokemon/imgs/Bellossom.png")

class Roselia(Grass):
    def __init__(self):
        moves = [
            Move("Magical Leaf", "GRASS", 60),
            Move("Mega Drain", "GRASS", 40),
            Move("Absorb", "GRASS", 20),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Roselia", 50, moves, "./TVPoke/Pokemon/imgs/Roselia.png")

class Cacnea(Grass):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Absorb", "GRASS", 20),
            Move("Poison Sting", "POISON", 15),
            Move("Pin Missile", "BUG", 14)
        ]
        super().__init__("Cacnea", 50, moves, "./TVPoke/Pokemon/imgs/Cacnea.png")

class Cacturne(Grass):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Absorb", "GRASS", 20),
            Move("Poison Sting", "POISON", 15),
            Move("Pin Missile", "BUG", 14)
        ]
        super().__init__("Cacturne", 70, moves, "./TVPoke/Pokemon/imgs/Cacturne.png")

class Tropius(Grass):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Razor Leaf", "GRASS", 55),
            Move("Gust", "FLYING", 40),
            Move("Whirlwind", "NORMAL", 0)
        ]
        super().__init__("Tropius", 99, moves, "./TVPoke/Pokemon/imgs/Tropius.png")
