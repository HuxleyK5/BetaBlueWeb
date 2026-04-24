class Pokemon:
    def __init__(self, name, hp, type, critType, moves, imgPath):
        self.name = name
        self.hp = hp
        self.MAXhp = hp
        self.type = type
        self.critType = critType
        self.moves = moves
        self.img = imgPath

    def takeDamage(self, move):
        multi = 1
        if move.type == self.critType:
            multi = 2
        self.hp -= move.damage * multi