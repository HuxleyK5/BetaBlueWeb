from TVPoke.BaseClasses.PokeTypes import Electric
from TVPoke.BaseClasses.Move import Move

class Electrike(Electric):
    def __init__(self):
        super().__init__("Electrike", 40, [
            Move("Tackle", "NORMAL", 40),
            Move("Thunder Wave", "ELECTRIC", 0),
            Move("Leer", "NORMAL", 0),
            Move("Howl", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Electrike.png")


class Manectric(Electric):
    def __init__(self):
        super().__init__("Manectric", 70, [
            Move("Tackle", "NORMAL", 40),
            Move("Bite", "DARK", 60),
            Move("Leer", "NORMAL", 0),
            Move("Discharge", "ELECTRIC", 80)
        ], "./TVPoke/Pokemon/imgs/Manectric.png")


class Plusle(Electric):
    def __init__(self):
        super().__init__("Plusle", 60, [
            Move("Growl", "NORMAL", 0),
            Move("Thunder Wave", "ELECTRIC", 0),
            Move("Quick Attack", "NORMAL", 40),
            Move("Helping Hand", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Plusle.png")


class Minun(Electric):
    def __init__(self):
        super().__init__("Minun", 60, [
            Move("Growl", "NORMAL", 0),
            Move("Charm", "NORMAL", 0),
            Move("Quick Attack", "NORMAL", 40),
            Move("Spark", "ELECTRIC", 65)
        ], "./TVPoke/Pokemon/imgs/Minun.png")


class Magnemite(Electric):
    def __init__(self):
        super().__init__("Magnemite", 25, [
            Move("Metal Sound", "STEEL", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Thunder Shock", "ELECTRIC", 40),
            Move("Supersonic", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Magnemite.png")


class Magneton(Electric):
    def __init__(self):
        super().__init__("Magneton", 50, [
            Move("Metal Sound", "STEEL", 0),
            Move("Bullet Punch", "STEEL", 40),
            Move("Thunder Shock", "ELECTRIC", 40),
            Move("Magnet Rise", "ELECTRIC", 0)
        ], "./TVPoke/Pokemon/imgs/Magneton.png")


class Voltorb(Electric):
    def __init__(self):
        super().__init__("Voltorb", 40, [
            Move("Charge", "ELECTRIC", 0),
            Move("Tackle", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Sonic Boom", "NORMAL", 0)
        ], "./TVPoke/Pokemon/imgs/Voltorb.png")


class Electrode(Electric):
    def __init__(self):
        super().__init__("Electrode", 60, [
            Move("Charge", "ELECTRIC", 0),
            Move("Quick Attack", "NORMAL", 40),
            Move("Screech", "NORMAL", 0),
            Move("Thunder", "ELECTRIC", 110)
        ], "./TVPoke/Pokemon/imgs/Electrode.png")


class Pichu(Electric):
    def __init__(self):
        super().__init__("Pichu", 20, [
            Move("Thunder Shock", "ELECTRIC", 40),
            Move("Charm", "NORMAL", 0),
            Move("Tail Whip", "NORMAL", 0),
            Move("Thunder Wave", "ELECTRIC", 0)
        ], "./TVPoke/Pokemon/imgs/Pichu.png")


class Pikachu(Electric):
    def __init__(self):
        super().__init__("Pikachu", 35, [
            Move("Quick Attack", "NORMAL", 40),
            Move("Growl", "NORMAL", 0),
            Move("Tail Whip", "NORMAL", 0),
            Move("Thunderbolt", "ELECTRIC", 90)
        ], "./TVPoke/Pokemon/imgs/Pikachu.png")


class Raichu(Electric):
    def __init__(self):
        super().__init__("Raichu", 60, [
            Move("Thunder Shock", "ELECTRIC", 40),
            Move("Iron Tail", "STEEL", 100),
            Move("Quick Attack", "NORMAL", 40),
            Move("Thunderbolt", "ELECTRIC", 90)
        ], "./TVPoke/Pokemon/imgs/Raichu.png")
