from TVPoke.BaseClasses.PokeTypes import Electric
from TVPoke.BaseClasses.Move import Move

class Electrike(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Quick Attack", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Roar", "NORMAL", 0)
        ]
        super().__init__("Electrike", 40, moves, "./TVPoke/Pokemon/imgs/Electrike.png")

class Manectric(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Quick Attack", "NORMAL", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Odor Sleuth", "NORMAL", 0)
        ]
        super().__init__("Manectric", 70, moves, "./TVPoke/Pokemon/imgs/Manectric.png")

class Plusle(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Quick Attack", "NORMAL", 40),
            Move("Fake Tears", "DARK", 0),
            Move("Encore", "NORMAL", 0)
        ]
        super().__init__("Plusle", 60, moves, "./TVPoke/Pokemon/imgs/Plusle.png")

class Minun(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("Quick Attack", "NORMAL", 40),
            Move("Charm", "NORMAL", 0),
            Move("Encore", "NORMAL", 0)
        ]
        super().__init__("Minun", 60, moves, "./TVPoke/Pokemon/imgs/Minun.png")

class Magnemite(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("ThunderShock", "ELECTRIC", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Thunder Wave", "ELECTRIC", 0)
        ]
        super().__init__("Magnemite", 25, moves, "./TVPoke/Pokemon/imgs/Magnemite.png")

class Magneton(Electric):
    def __init__(self):
        moves = [
            Move("Spark", "ELECTRIC", 65),
            Move("ThunderShock", "ELECTRIC", 40),
            Move("Tackle", "NORMAL", 35),
            Move("Thunder Wave", "ELECTRIC", 0)
        ]
        super().__init__("Magneton", 50, moves, "./TVPoke/Pokemon/imgs/Magneton.png")

class Voltorb(Electric):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Spark", "ELECTRIC", 65),
            Move("Tackle", "NORMAL", 35),
            Move("SonicBoom", "NORMAL", 0)
        ]
        super().__init__("Voltorb", 40, moves, "./TVPoke/Pokemon/imgs/Voltorb.png")

class Electrode(Electric):
    def __init__(self):
        moves = [
            Move("Selfdestruct", "NORMAL", 200),
            Move("Spark", "ELECTRIC", 65),
            Move("Tackle", "NORMAL", 35),
            Move("SonicBoom", "NORMAL", 0)
        ]
        super().__init__("Electrode", 60, moves, "./TVPoke/Pokemon/imgs/Electrode.png")

class Pichu(Electric):
    def __init__(self):
        moves = [
            Move("ThunderShock", "ELECTRIC", 40),
            Move("Sweet Kiss", "NORMAL", 0),
            Move("Thunder Wave", "ELECTRIC", 0),
            Move("Tail Whip", "NORMAL", 0)
        ]
        super().__init__("Pichu", 20, moves, "./TVPoke/Pokemon/imgs/Pichu.png")

class Pikachu(Electric):
    def __init__(self):
        moves = [
            Move("Thunderbolt", "ELECTRIC", 95),
            Move("Slam", "NORMAL", 80),
            Move("Quick Attack", "NORMAL", 40),
            Move("ThunderShock", "ELECTRIC", 40)
        ]
        super().__init__("Pikachu", 35, moves, "./TVPoke/Pokemon/imgs/Pikachu.png")

class Raichu(Electric):
    def __init__(self):
        moves = [
            Move("Thunderbolt", "ELECTRIC", 95),
            Move("ThunderShock", "ELECTRIC", 40),
            Move("Quick Attack", "NORMAL", 40),
            Move("Tail Whip", "NORMAL", 0)
        ]
        super().__init__("Raichu", 60, moves, "./TVPoke/Pokemon/imgs/Raichu.png")
