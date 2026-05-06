from TVPoke.BaseClasses.PokeTypes import Normal
from TVPoke.BaseClasses.Move import Move

class Zigzagoon(Normal):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Covet", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Pin Missile", "BUG", 14)
        ]
        super().__init__("Zigzagoon", 38, moves, "./TVPoke/Pokemon/imgs/Zigzagoon.png")

class Linoone(Normal):
    def __init__(self):
        moves = [
            Move("Headbutt", "NORMAL", 70),
            Move("Tackle", "NORMAL", 35),
            Move("Fury Swipes", "NORMAL", 18),
            Move("Mud Sport", "GROUND", 0)
        ]
        super().__init__("Linoone", 78, moves, "./TVPoke/Pokemon/imgs/Linoone.png")

class Slakoth(Normal):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Scratch", "NORMAL", 40),
            Move("Amnesia", "PSYCHIC", 0),
            Move("Slack Off", "NORMAL", 0)
        ]
        super().__init__("Slakoth", 60, moves, "./TVPoke/Pokemon/imgs/Slakoth.png")

class Vigoroth(Normal):
    def __init__(self):
        moves = [
            Move("Uproar", "NORMAL", 50),
            Move("Scratch", "NORMAL", 40),
            Move("Fury Swipes", "NORMAL", 18),
            Move("Endure", "NORMAL", 0)
        ]
        super().__init__("Vigoroth", 80, moves, "./TVPoke/Pokemon/imgs/Vigoroth.png")

class Slaking(Normal):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Scratch", "NORMAL", 40),
            Move("Amnesia", "PSYCHIC", 0),
            Move("Yawn", "NORMAL", 0)
        ]
        super().__init__("Slaking", 150, moves, "./TVPoke/Pokemon/imgs/Slaking.png")

class Whismur(Normal):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Uproar", "NORMAL", 50),
            Move("Pound", "NORMAL", 40),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Whismur", 64, moves, "./TVPoke/Pokemon/imgs/Whismur.png")

class Loudred(Normal):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Uproar", "NORMAL", 50),
            Move("Pound", "NORMAL", 40),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Loudred", 84, moves, "./TVPoke/Pokemon/imgs/Loudred.png")

class Exploud(Normal):
    def __init__(self):
        moves = [
            Move("Stomp", "NORMAL", 65),
            Move("Uproar", "NORMAL", 50),
            Move("Pound", "NORMAL", 40),
            Move("Astonish", "GHOST", 30)
        ]
        super().__init__("Exploud", 104, moves, "./TVPoke/Pokemon/imgs/Exploud.png")

class Skitty(Normal):
    def __init__(self):
        moves = [
            Move("Faint Attack", "DARK", 60),
            Move("Tackle", "NORMAL", 35),
            Move("DoubleSlap", "NORMAL", 15),
            Move("Charm", "NORMAL", 0)
        ]
        super().__init__("Skitty", 50, moves, "./TVPoke/Pokemon/imgs/Skitty.png")

class Delcatty(Normal):
    def __init__(self):
        moves = [
            Move("DoubleSlap", "NORMAL", 15),
            Move("Sing", "NORMAL", 0),
            Move("Growl", "NORMAL", 0),
            Move("Attract", "NORMAL", 0)
        ]
        super().__init__("Delcatty", 70, moves, "./TVPoke/Pokemon/imgs/Delcatty.png")

class Spinda(Normal):
    def __init__(self):
        moves = [
            Move("Dizzy Punch", "NORMAL", 70),
            Move("Psybeam", "PSYCHIC", 65),
            Move("Faint Attack", "DARK", 60),
            Move("Uproar", "NORMAL", 50)
        ]
        super().__init__("Spinda", 60, moves, "./TVPoke/Pokemon/imgs/Spinda.png")

class Castform(Normal):
    def __init__(self):
        moves = [
            Move("Weather Ball", "NORMAL", 50),
            Move("Water Gun", "WATER", 40),
            Move("Powder Snow", "ICE", 40),
            Move("Ember", "FIRE", 40)
        ]
        super().__init__("Castform", 70, moves, "./TVPoke/Pokemon/imgs/Castform.png")

class Kecleon(Normal):
    def __init__(self):
        moves = [
            Move("Psybeam", "PSYCHIC", 65),
            Move("Faint Attack", "DARK", 60),
            Move("Thief", "DARK", 40),
            Move("Scratch", "NORMAL", 40)
        ]
        super().__init__("Kecleon", 60, moves, "./TVPoke/Pokemon/imgs/Kecleon.png")

class Azurill(Normal):
    def __init__(self):
        moves = [
            Move("Slam", "NORMAL", 80),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("Tail Whip", "NORMAL", 0)
        ]
        super().__init__("Azurill", 50, moves, "./TVPoke/Pokemon/imgs/Azurill.png")

class Doduo(Normal):
    def __init__(self):
        moves = [
            Move("Tri Attack", "NORMAL", 80),
            Move("Pursuit", "DARK", 40),
            Move("Peck", "FLYING", 35),
            Move("Rage", "NORMAL", 20)
        ]
        super().__init__("Doduo", 35, moves, "./TVPoke/Pokemon/imgs/Doduo.png")

class Dodrio(Normal):
    def __init__(self):
        moves = [
            Move("Tri Attack", "NORMAL", 80),
            Move("Pursuit", "DARK", 40),
            Move("Peck", "FLYING", 35),
            Move("Rage", "NORMAL", 20)
        ]
        super().__init__("Dodrio", 60, moves, "./TVPoke/Pokemon/imgs/Dodrio.png")

class Swablu(Normal):
    def __init__(self):
        moves = [
            Move("Peck", "FLYING", 35),
            Move("Astonish", "GHOST", 30),
            Move("Fury Attack", "NORMAL", 15),
            Move("Mist", "ICE", 0)
        ]
        super().__init__("Swablu", 45, moves, "./TVPoke/Pokemon/imgs/Swablu.png")

class Zangoose(Normal):
    def __init__(self):
        moves = [
            Move("Slash", "NORMAL", 70),
            Move("Pursuit", "DARK", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Scratch", "NORMAL", 40)
        ]
        super().__init__("Zangoose", 73, moves, "./TVPoke/Pokemon/imgs/Zangoose.png")

class Igglybuff(Normal):
    def __init__(self):
        moves = [
            Move("Pound", "NORMAL", 40),
            Move("Sweet Kiss", "NORMAL", 0),
            Move("Defense Curl", "NORMAL", 0),
            Move("Sing", "NORMAL", 0)
        ]
        super().__init__("Igglybuff", 90, moves, "./TVPoke/Pokemon/imgs/Igglybuff.png")

class Jigglypuff(Normal):
    def __init__(self):
        moves = [
            Move("Pound", "NORMAL", 40),
            Move("Rollout", "ROCK", 30),
            Move("DoubleSlap", "NORMAL", 15),
            Move("Rest", "PSYCHIC", 0)
        ]
        super().__init__("Jigglypuff", 115, moves, "./TVPoke/Pokemon/imgs/Jigglypuff.png")

class Wigglytuff(Normal):
    def __init__(self):
        moves = [
            Move("DoubleSlap", "NORMAL", 15),
            Move("Sing", "NORMAL", 0),
            Move("Disable", "NORMAL", 0),
            Move("Defense Curl", "NORMAL", 0)
        ]
        super().__init__("Wigglytuff", 140, moves, "./TVPoke/Pokemon/imgs/Wigglytuff.png")
