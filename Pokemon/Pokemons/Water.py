from TVPoke.BaseClasses.PokeTypes import Water
from TVPoke.BaseClasses.Move import Move

class Mudkip(Water):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Water Gun", "WATER", 40),
            Move("Mud Slap", "GROUND", 20),
            Move("Foresight", "NORMAL", 0)
        ]
        super().__init__("Mudkip", 50, moves, "./TVPoke/Pokemon/imgs/Mudkip.png")

class Marshtomp(Water):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Water Gun", "WATER", 40),
            Move("Mud Shot", "GROUND", 55),
            Move("Aqua Ring", "WATER", 0)
        ]
        super().__init__("Marshtomp", 70, moves, "./TVPoke/Pokemon/imgs/Marshtomp.png")

class Swampert(Water):
    def __init__(self):
        moves = [
            Move("Tackle", "NORMAL", 40),
            Move("Water Gun", "WATER", 40),
            Move("Earthquake", "GROUND", 100),
            Move("Hydro Pump", "WATER", 110)
        ]
        super().__init__("Swampert", 100, moves, "./TVPoke/Pokemon/imgs/Swampert.png")



class Wingull(Water):
    def __init__(self):
        super().__init__("Wingull", 40, [
            Move("Water Gun", "WATER", 40),
            Move("Supersonic", "NORMAL", 0),
            Move("Wing Attack", "FLYING", 60),
            Move("Mist", "ICE", 0)
        ], "./TVPoke/Pokemon/imgs/Wingull.png")

class Pelipper(Water):
    def __init__(self):
        super().__init__("Pelipper", 60, [
            Move("Water Gun", "WATER", 40),
            Move("Protect", "NORMAL", 0),
            Move("Wing Attack", "FLYING", 60),
            Move("Roost", "FLYING", 0)
        ], "./TVPoke/Pokemon/imgs/Pelipper.png")

class Goldeen(Water):
    def __init__(self):
        super().__init__("Goldeen", 45, [
            Move("Peck", "FLYING", 35),
            Move("Tail Whip", "NORMAL", 0),
            Move("Water Sport", "WATER", 0),
            Move("Supersonic", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Goldeen.png")

class Seaking(Water):
    def __init__(self):
        super().__init__("Seaking", 80, [
            Move("Horn Attack", "NORMAL", 65),
            Move("Tail Whip", "NORMAL", 0),
            Move("Water Pulse", "WATER", 60),
            Move("Drill Run", "GROUND", 95)
        ], "./TVPoke/Pokemon/imgs/Seaking.png")

class Magikarp(Water):
    def __init__(self):
        super().__init__("Magikarp", 20, [
            Move("Splash", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40)
        ], "./TVPoke/Pokemon/imgs/Magikarp.png")

class Gyarados(Water):
    def __init__(self):
        super().__init__("Gyarados", 95, [
            Move("Thrash", "NORMAL", 120),
            Move("Bite", "DARK", 60),
            Move("Dragon Rage", "DRAGON", 0),
            Move("Leer", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Gyarados.png")

class Marill(Water):
    def __init__(self):
        super().__init__("Marill", 70, [
            Move("Tackle", "NORMAL", 40),
            Move("Defense Curl", "NORMAL", 0),
            Move("Tail Whip", "NORMAL", 0),
            Move("Water Gun", "WATER", 40)
        ], "./TVPoke/Pokemon/imgs/Marill.png")

class Azumarill(Water):
    def __init__(self):
        super().__init__("Azumarill", 100, [
            Move("Tackle", "NORMAL", 40),
            Move("Belly Drum", "NORMAL", 0),
            Move("Waterfall", "WATER", 80),
            Move("Play Rough", "FAIRY", 90)
        ], "./TVPoke/Pokemon/imgs/Azumarill.png")

class Tentacool(Water):
    def __init__(self):
        super().__init__("Tentacool", 40, [
            Move("Poison Sting", "POISON", 15),
            Move("Supersonic", "NORMAL", 0),
            Move("Constrict", "NORMAL", 10),
            Move("Acid", "POISON", 40)
        ], "./TVPoke/Pokemon/imgs/Tentacool.png")

class Tentacruel(Water):
    def __init__(self):
        super().__init__("Tentacruel", 80, [
            Move("Poison Sting", "POISON", 15),
            Move("Toxic Spikes", "POISON", 0),
            Move("Constrict", "NORMAL", 10),
            Move("Hydro Pump", "WATER", 110)
        ], "./TVPoke/Pokemon/imgs/Tentacruel.png")

class Carvanha(Water):
    def __init__(self):
        super().__init__("Carvanha", 45, [
            Move("Leer", "NORMAL", 0),
            Move("Bite", "DARK", 60),
            Move("Rage", "NORMAL", 20),
            Move("Focus Energy", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Carvanha.png")

class Sharpedo(Water):
    def __init__(self):
        super().__init__("Sharpedo", 70, [
            Move("Leer", "NORMAL", 0),
            Move("Bite", "DARK", 60),
            Move("Aqua Jet", "WATER", 65),
            Move("Crunch", "DARK", 80)
        ], "./TVPoke/Pokemon/imgs/Sharpedo.png")

class Wailmer(Water):
    def __init__(self):
        super().__init__("Wailmer", 130, [
            Move("Splash", "NORMAL", 0),
            Move("Growl", "NORMAL", 0),
            Move("Water Gun", "WATER", 40),
            Move("Rollout", "ROCK", 30)
        ], "./TVPoke/Pokemon/imgs/Wailmer.png")

class Wailord(Water):
    def __init__(self):
        super().__init__("Wailord", 170, [
            Move("Water Gun", "WATER", 40),
            Move("Mist", "ICE", 0),
            Move("Rest", "PSYCHIC", 0),
            Move("Hydro Pump", "WATER", 110)
        ], "./TVPoke/Pokemon/imgs/Wailord.png")

class Barboach(Water):
    def __init__(self):
        super().__init__("Barboach", 50, [
            Move("Mud Slap", "GROUND", 20),
            Move("Water Sport", "WATER", 0),
            Move("Water Gun", "WATER", 40),
            Move("Magnitude", "GROUND", 0)
        ], "./TVPoke/Pokemon/imgs/Barboach.png")

class Whiscash(Water):
    def __init__(self):
        super().__init__("Whiscash", 110, [
            Move("Mud Shot", "GROUND", 55),
            Move("Water Sport", "WATER", 0),
            Move("Water Pulse", "WATER", 60),
            Move("Earthquake", "GROUND", 100)
        ], "./TVPoke/Pokemon/imgs/Whiscash.png")

class Corphish(Water):
    def __init__(self):
        super().__init__("Corphish", 43, [
            Move("Bubble", "WATER", 40),
            Move("Harden", "NORMAL", 0),
            Move("Vice Grip", "NORMAL", 55),
            Move("Leer", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Corphish.png")

class Crawdaunt(Water):
    def __init__(self):
        super().__init__("Crawdaunt", 63, [
            Move("Bubble", "WATER", 40),
            Move("Taunt", "DARK", 0),
            Move("Crabhammer", "WATER", 100),
            Move("Crunch", "DARK", 80)
        ], "./TVPoke/Pokemon/imgs/Crawdaunt.png")

class Feebas(Water):
    def __init__(self):
        super().__init__("Feebas", 20, [
            Move("Splash", "NORMAL", 0),
            Move("Tackle", "NORMAL", 40)
        ], "./TVPoke/Pokemon/imgs/Feebas.png")

class Milotic(Water):
    def __init__(self):
        super().__init__("Milotic", 95, [
            Move("Water Gun", "WATER", 40),
            Move("Wrap", "NORMAL", 15),
            Move("Water Sport", "WATER", 0),
            Move("Refresh", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Milotic.png")

class Staryu(Water):
    def __init__(self):
        super().__init__("Staryu", 30, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Water Gun", "WATER", 40),
            Move("Rapid Spin", "NORMAL", 50)
        ], "./TVPoke/Pokemon/imgs/Staryu.png")

class Starmie(Water):
    def __init__(self):
        super().__init__("Starmie", 60, [
            Move("Swift", "NORMAL", 60),
            Move("Recover", "NORMAL", 0),
            Move("Water Pulse", "WATER", 60),
            Move("Psychic", "PSYCHIC", 90)
        ], "./TVPoke/Pokemon/imgs/Starmie.png")

class Psyduck(Water):
    def __init__(self):
        super().__init__("Psyduck", 50, [
            Move("Scratch", "NORMAL", 40),
            Move("Tail Whip", "NORMAL", 0),
            Move("Water Sport", "WATER", 0),
            Move("Disable", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Psyduck.png")

class Golduck(Water):
    def __init__(self):
        super().__init__("Golduck", 80, [
            Move("Scratch", "NORMAL", 40),
            Move("Confusion", "PSYCHIC", 50),
            Move("Water Pulse", "WATER", 60),
            Move("Disable", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Golduck.png")

class Clamperl(Water):
    def __init__(self):
        super().__init__("Clamperl", 35, [
            Move("Clamp", "WATER", 35),
            Move("Water Gun", "WATER", 40),
            Move("Whirlpool", "WATER", 35),
            Move("Iron Defense", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Clamperl.png")

class Huntail(Water):
    def __init__(self):
        super().__init__("Huntail", 55, [
            Move("Whirlpool", "WATER", 35),
            Move("Bite", "DARK", 60),
            Move("Screech", "NORMAL", 0),
            Move("Water Pulse", "WATER", 60)
        ], "./TVPoke/Pokemon/imgs/Huntail.png")

class Gorebyss(Water):
    def __init__(self):
        super().__init__("Gorebyss", 55, [
            Move("Whirlpool", "WATER", 35),
            Move("Confusion", "PSYCHIC", 50),
            Move("Agility", "PSYCHIC", 0),
            Move("Water Pulse", "WATER", 60)
        ], "./TVPoke/Pokemon/imgs/Gorebyss.png")

class Relicanth(Water):
    def __init__(self):
        super().__init__("Relicanth", 100, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Water Gun", "WATER", 40),
            Move("Ancient Power", "ROCK", 60)
        ], "./TVPoke/Pokemon/imgs/Relicanth.png")

class Corsola(Water):
    def __init__(self):
        super().__init__("Corsola", 65, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Bubble", "WATER", 40),
            Move("Recovery", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Corsola.png")

class Luvdisc(Water):
    def __init__(self):
        super().__init__("Luvdisc", 43, [
            Move("Tackle", "NORMAL", 40),
            Move("Charm", "NORMAL", 0),
            Move("Water Gun", "WATER", 40),
            Move("Agility", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Luvdisc.png")

class Horsea(Water):
    def __init__(self):
        super().__init__("Horsea", 30, [
            Move("Bubble", "WATER", 40),
            Move("SmokeScreen", "NORMAL", 0),
            Move("Leer", "NORMAL", 0),
            Move("Water Gun", "WATER", 40)
        ], "./TVPoke/Pokemon/imgs/Horsea.png")

class Seadra(Water):
    def __init__(self):
        super().__init__("Seadra", 55, [
            Move("Bubble", "WATER", 40),
            Move("SmokeScreen", "NORMAL", 0),
            Move("Leer", "NORMAL", 0),
            Move("Twister", "DRAGON", 40)
        ], "./TVPoke/Pokemon/imgs/Seadra.png")

class Kingdra(Water):
    def __init__(self):
        super().__init__("Kingdra", 75, [
            Move("Water Gun", "WATER", 40),
            Move("Smokescreen", "NORMAL", 0),
            Move("Dragon Breath", "DRAGON", 60),
            Move("Hydro Pump", "WATER", 110)
        ], "./TVPoke/Pokemon/imgs/Kingdra.png")

class Kyogre(Water):
    def __init__(self):
        super().__init__("Kyogre", 100, [
            Move("Water Pulse", "WATER", 60),
            Move("Scary Face", "NORMAL", 0),
            Move("Ancient Power", "ROCK", 60),
            Move("Water Spout", "WATER", 150)
        ], "./TVPoke/Pokemon/imgs/Kyogre.png")

class Chinchou(Water):
    def __init__(self):
        super().__init__("Chinchou", 75, [
            Move("Bubble", "WATER", 40),
            Move("Thunder Wave", "ELECTRIC", 0),
            Move("Supersonic", "NORMAL", 0),
            Move("Flail", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Chinchou.png")

class Lanturn(Water):
    def __init__(self):
        super().__init__("Lanturn", 125, [
            Move("Water Gun", "WATER", 40),
            Move("Thunder Wave", "ELECTRIC", 0),
            Move("Supersonic", "NORMAL", 0),
            Move("Discharge", "ELECTRIC", 80)
        ], "./TVPoke/Pokemon/imgs/Lanturn.png")
