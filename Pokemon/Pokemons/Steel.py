from TVPoke.BaseClasses.PokeTypes import Steel
from TVPoke.BaseClasses.Move import Move
from random import randint

class Mawile(Steel):
    def __init__(self):
        super().__init__("Mawile", 50, [
            Move("Astonish", "GHOST", 30),
            Move("Vice Grip", "NORMAL", 55),
            Move("Focus Energy", "NORMAL", 0),
            Move("Iron Head", "STEEL", 80)
        ], "./TVPoke/Pokemon/imgs/Mawile.png")

class Aron(Steel):
    def __init__(self):
        super().__init__("Aron", 50, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Mud Slap", "GROUND", 20),
            Move("Metal Claw", "STEEL", 50)
        ], "./TVPoke/Pokemon/imgs/Aron.png")

class Lairon(Steel):
    def __init__(self):
        super().__init__("Lairon", 60, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Mud Slap", "GROUND", 20),
            Move("Metal Burst", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Lairon.png")

class Aggron(Steel):
    def __init__(self):
        super().__init__("Aggron", 70, [
            Move("Tackle", "NORMAL", 40),
            Move("Harden", "NORMAL", 0),
            Move("Mud Slap", "GROUND", 20),
            Move("Heavy Slam", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Aggron.png")

class Beldum(Steel):
    def __init__(self):
        super().__init__("Beldum", 40, [
            Move("Take Down", "NORMAL", 90),
            Move("Metal Sound", "STEEL", 0),
            Move("Magnet Rise", "ELECTRIC", 0),
            Move("Meteor Mash", "STEEL", 90)
        ], "./TVPoke/Pokemon/imgs/Beldum.png")

class Metang(Steel):
    def __init__(self):
        super().__init__("Metang", 60, [
            Move("Take Down", "NORMAL", 90),
            Move("Metal Sound", "STEEL", 0),
            Move("Magnet Rise", "ELECTRIC", 0),
            Move("Iron Defense", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Metang.png")

class Metagross(Steel):
    def __init__(self):
        super().__init__("Metagross", 80, [
            Move("Take Down", "NORMAL", 90),
            Move("Metal Sound", "STEEL", 0),
            Move("Psychic", "PSYCHIC", 90),
            Move("Meteor Mash", "STEEL", 90)
        ], "./TVPoke/Pokemon/imgs/Metagross.png")

class Registeel(Steel):
    def __init__(self):
        super().__init__("Registeel", 80, [
            Move("Curse", "GHOST", 0),
            Move("Superpower", "FIGHTING", 120),
            Move("Iron Defense", "STEEL", 0),
            Move("Flash Cannon", "STEEL", 80)
        ], "./TVPoke/Pokemon/imgs/Registeel.png")



class Skarmory(Steel):
    def __init__(self):
        super().__init__("Skarmory", 65, [
            Move("Peck", "FLYING", 35),
            Move("Protect", "NORMAL", 0),
            Move("Metal Sound", "STEEL", 0),
            Move("Iron Defense", "STEEL", 0)
        ], "./TVPoke/Pokemon/imgs/Skarmory.png")

class Jirachi(Steel):
    def __init__(self):
        super().__init__("Jirachi", 100, [
            Move("Confusion", "PSYCHIC", 50),
            Move("Wish", "NORMAL", 0),
            Move("Doom Desire", "STEEL", 130),
            Move("Gravity", "PSYCHIC", 0)
        ], "./TVPoke/Pokemon/imgs/Jirachi.png")

