from TVPoke.BaseClasses.PokeTypes import Water
from TVPoke.BaseClasses.Move import Move

class Mudkip(Water):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Mud-Slap", "GROUND", 20)
        ]
        super().__init__("Mudkip", 50, moves, "./TVPoke/Pokemon/imgs/Mudkip.png")

class Marshtomp(Water):
    def __init__(self):
        moves = [
            Move("Mud Shot", "GROUND", 55),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Mud-Slap", "GROUND", 20)
        ]
        super().__init__("Marshtomp", 70, moves, "./TVPoke/Pokemon/imgs/Marshtomp.png")

class Swampert(Water):
    def __init__(self):
        moves = [
            Move("Mud Shot", "GROUND", 55),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Mud-Slap", "GROUND", 20)
        ]
        super().__init__("Swampert", 100, moves, "./TVPoke/Pokemon/imgs/Swampert.png")

class Wingull(Water):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Water Gun", "WATER", 40),
            Move("Mist", "ICE", 0),
            Move("Supersonic", "NORMAL", 0)
        ]
        super().__init__("Wingull", 40, moves, "./TVPoke/Pokemon/imgs/Wingull.png")

class Pelipper(Water):
    def __init__(self):
        moves = [
            Move("Wing Attack", "FLYING", 60),
            Move("Water Gun", "WATER", 40),
            Move("Protect", "NORMAL", 0),
            Move("Mist", "ICE", 0)
        ]
        super().__init__("Pelipper", 60, moves, "./TVPoke/Pokemon/imgs/Pelipper.png")

class Goldeen(Water):
    def __init__(self):
        moves = [
            Move("Horn Attack", "NORMAL", 65),
            Move("Peck", "FLYING", 35),
            Move("Fury Attack", "NORMAL", 15),
            Move("Flail", "NORMAL", 0)
        ]
        super().__init__("Goldeen", 45, moves, "./TVPoke/Pokemon/imgs/Goldeen.png")

class Seaking(Water):
    def __init__(self):
        moves = [
            Move("Horn Attack", "NORMAL", 65),
            Move("Peck", "FLYING", 35),
            Move("Fury Attack", "NORMAL", 15),
            Move("Flail", "NORMAL", 0)
        ]
        super().__init__("Seaking", 80, moves, "./TVPoke/Pokemon/imgs/Seaking.png")

class Magikarp(Water):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 35),
            Move("Flail", "NORMAL", 0),
            Move("Splash", "NORMAL", 0)
        ]
        super().__init__("Magikarp", 20, moves, "./TVPoke/Pokemon/imgs/Magikarp.png")

class Gyarados(Water):
    def __init__(self):
        moves = [
            Move("Thrash", "NORMAL", 90),
            Move("Bite", "DARK", 60),
            Move("Leer", "NORMAL", 0),
            Move("Dragon Rage", "DRAGON", 0)
        ]
        super().__init__("Gyarados", 95, moves, "./TVPoke/Pokemon/imgs/Gyarados.png")

class Marill(Water):
    def __init__(self):
        moves = [
            Move("Double-Edge", "NORMAL", 120),
            Move("BubbleBeam", "WATER", 65),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35)
        ]
        super().__init__("Marill", 70, moves, "./TVPoke/Pokemon/imgs/Marill.png")

class Azumarill(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Azumarill", 100, moves, "./TVPoke/Pokemon/imgs/Azumarill.png")

class Tentacool(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Acid", "POISON", 40),
            Move("Wrap", "NORMAL", 15),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Tentacool", 40, moves, "./TVPoke/Pokemon/imgs/Tentacool.png")

class Tentacruel(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Acid", "POISON", 40),
            Move("Wrap", "NORMAL", 15),
            Move("Poison Sting", "POISON", 15)
        ]
        super().__init__("Tentacruel", 80, moves, "./TVPoke/Pokemon/imgs/Tentacruel.png")

class Carvanha(Water):
    def __init__(self):
        moves = [
            Move("Crunch", "DARK", 80),
            Move("Bite", "DARK", 60),
            Move("Rage", "NORMAL", 20),
            Move("Screech", "NORMAL", 0)
        ]
        super().__init__("Carvanha", 45, moves, "./TVPoke/Pokemon/imgs/Carvanha.png")

class Sharpedo(Water):
    def __init__(self):
        moves = [
            Move("Crunch", "DARK", 80),
            Move("Bite", "DARK", 60),
            Move("Rage", "NORMAL", 20),
            Move("Screech", "NORMAL", 0)
        ]
        super().__init__("Sharpedo", 70, moves, "./TVPoke/Pokemon/imgs/Sharpedo.png")

class Wailmer(Water):
    def __init__(self):
        moves = [
            Move("Water Pulse", "WATER", 60),
            Move("Water Gun", "WATER", 40),
            Move("Astonish", "GHOST", 30),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Wailmer", 130, moves, "./TVPoke/Pokemon/imgs/Wailmer.png")

class Wailord(Water):
    def __init__(self):
        moves = [
            Move("Water Pulse", "WATER", 60),
            Move("Water Gun", "WATER", 40),
            Move("Astonish", "GHOST", 30),
            Move("Rollout", "ROCK", 30)
        ]
        super().__init__("Wailord", 170, moves, "./TVPoke/Pokemon/imgs/Wailord.png")

class Barboach(Water):
    def __init__(self):
        moves = [
            Move("Snore", "NORMAL", 40),
            Move("Water Gun", "WATER", 40),
            Move("Mud-Slap", "GROUND", 20),
            Move("Rest", "PSYCHIC", 0)
        ]
        super().__init__("Barboach", 50, moves, "./TVPoke/Pokemon/imgs/Barboach.png")

class Whiscash(Water):
    def __init__(self):
        moves = [
            Move("Snore", "NORMAL", 40),
            Move("Water Gun", "WATER", 40),
            Move("Mud-Slap", "GROUND", 20),
            Move("Rest", "PSYCHIC", 0)
        ]
        super().__init__("Whiscash", 110, moves, "./TVPoke/Pokemon/imgs/Whiscash.png")

class Corphish(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("ViceGrip", "NORMAL", 55),
            Move("Knock Off", "DARK", 20),
            Move("Bubble", "WATER", 20)
        ]
        super().__init__("Corphish", 43, moves, "./TVPoke/Pokemon/imgs/Corphish.png")

class Crawdaunt(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("ViceGrip", "NORMAL", 55),
            Move("Knock Off", "DARK", 20),
            Move("Bubble", "WATER", 20)
        ]
        super().__init__("Crawdaunt", 63, moves, "./TVPoke/Pokemon/imgs/Crawdaunt.png")

class Feebas(Water):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 35),
            Move("Flail", "NORMAL", 0),
            Move("Splash", "NORMAL", 0)
        ]
        super().__init__("Feebas", 20, moves, "./TVPoke/Pokemon/imgs/Feebas.png")

class Milotic(Water):
    def __init__(self):
        moves = [
            Move("Water Pulse", "WATER", 60),
            Move("Twister", "DRAGON", 40),
            Move("Water Gun", "WATER", 40),
            Move("Wrap", "NORMAL", 15)
        ]
        super().__init__("Milotic", 95, moves, "./TVPoke/Pokemon/imgs/Milotic.png")

class Staryu(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Swift", "NORMAL", 60),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35)
        ]
        super().__init__("Staryu", 30, moves, "./TVPoke/Pokemon/imgs/Staryu.png")

class Starmie(Water):
    def __init__(self):
        moves = [
            Move("Swift", "NORMAL", 60),
            Move("Water Gun", "WATER", 40),
            Move("Rapid Spin", "NORMAL", 20),
            Move("Recover", "NORMAL", 0)
        ]
        super().__init__("Starmie", 60, moves, "./TVPoke/Pokemon/imgs/Starmie.png")

class Psyduck(Water):
    def __init__(self):
        moves = [
            Move("Confusion", "PSYCHIC", 50),
            Move("Scratch", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Disable", "NORMAL", 0)
        ]
        super().__init__("Psyduck", 50, moves, "./TVPoke/Pokemon/imgs/Psyduck.png")

class Golduck(Water):
    def __init__(self):
        moves = [
            Move("Confusion", "PSYCHIC", 50),
            Move("Scratch", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Water Sport", "WATER", 0)
        ]
        super().__init__("Golduck", 80, moves, "./TVPoke/Pokemon/imgs/Golduck.png")

class Clamperl(Water):
    def __init__(self):
        moves = [
            Move("Water Gun", "WATER", 40),
            Move("Clamp", "WATER", 35),
            Move("Whirlpool", "WATER", 15),
            Move("Iron Defense", "STEEL", 0)
        ]
        super().__init__("Clamperl", 35, moves, "./TVPoke/Pokemon/imgs/Clamperl.png")

class Huntail(Water):
    def __init__(self):
        moves = [
            Move("Water Pulse", "WATER", 60),
            Move("Bite", "DARK", 60),
            Move("Whirlpool", "WATER", 15),
            Move("Scary Face", "NORMAL", 0)
        ]
        super().__init__("Huntail", 55, moves, "./TVPoke/Pokemon/imgs/Huntail.png")

class Gorebyss(Water):
    def __init__(self):
        moves = [
            Move("Water Pulse", "WATER", 60),
            Move("Confusion", "PSYCHIC", 50),
            Move("Whirlpool", "WATER", 15),
            Move("Amnesia", "PSYCHIC", 0)
        ]
        super().__init__("Gorebyss", 55, moves, "./TVPoke/Pokemon/imgs/Gorebyss.png")

class Relicanth(Water):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Rock Tomb", "ROCK", 50),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35)
        ]
        super().__init__("Relicanth", 100, moves, "./TVPoke/Pokemon/imgs/Relicanth.png")

class Corsola(Water):
    def __init__(self):
        moves = [
            Move("BubbleBeam", "WATER", 65),
            Move("Tackle", "NORMAL", 35),
            Move("Spike Cannon", "NORMAL", 20),
            Move("Bubble", "WATER", 20)
        ]
        super().__init__("Corsola", 65, moves, "./TVPoke/Pokemon/imgs/Corsola.png")

class Luvdisc(Water):
    def __init__(self):
        moves = [
            Move("Take Down", "NORMAL", 90),
            Move("Water Gun", "WATER", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Attract", "NORMAL", 0)
        ]
        super().__init__("Luvdisc", 43, moves, "./TVPoke/Pokemon/imgs/Luvdisc.png")

class Horsea(Water):
    def __init__(self):
        moves = [
            Move("Twister", "DRAGON", 40),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("Leer", "NORMAL", 0)
        ]
        super().__init__("Horsea", 30, moves, "./TVPoke/Pokemon/imgs/Horsea.png")

class Seadra(Water):
    def __init__(self):
        moves = [
            Move("Twister", "DRAGON", 40),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("SmokeScreen", "NORMAL", 0)
        ]
        super().__init__("Seadra", 55, moves, "./TVPoke/Pokemon/imgs/Seadra.png")

class Kingdra(Water):
    def __init__(self):
        moves = [
            Move("Twister", "DRAGON", 40),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("SmokeScreen", "NORMAL", 0)
        ]
        super().__init__("Kingdra", 75, moves, "./TVPoke/Pokemon/imgs/Kingdra.png")

class Kyogre(Water):
    def __init__(self):
        moves = [
            Move("Body Slam", "NORMAL", 85),
            Move("AncientPower", "ROCK", 60),
            Move("Water Pulse", "WATER", 60),
            Move("Calm Mind", "PSYCHIC", 0)
        ]
        super().__init__("Kyogre", 100, moves, "./TVPoke/Pokemon/imgs/Kyogre.png")

class Chinchou(Water):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("Confuse Ray", "GHOST", 0)
        ]
        super().__init__("Chinchou", 75, moves, "./TVPoke/Pokemon/imgs/Chinchou.png")

class Lanturn(Water):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Water Gun", "WATER", 40),
            Move("Bubble", "WATER", 20),
            Move("Flail", "NORMAL", 0)
        ]
        super().__init__("Lanturn", 125, moves, "./TVPoke/Pokemon/imgs/Lanturn.png")
