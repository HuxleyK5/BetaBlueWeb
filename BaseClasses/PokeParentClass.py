EVOLUTION_LEVELS = {
    "Treecko": (16, "Grovyle"),
    "Grovyle": (36, "Sceptile"),
    "Torchic": (16, "Combusken"),
    "Combusken": (36, "Blaziken"),
    "Mudkip": (16, "Marshtomp"),
    "Marshtomp": (36, "Swampert"),
    "Lotad": (14, "Lombre"),
    "Lombre": (36, "Ludicolo"),
    "Seedot": (14, "Nuzleaf"),
    "Nuzleaf": (32, "Shiftry"),
    "Shroomish": (23, "Breloom"),
    "Oddish": (21, "Gloom"),
    "Gloom": (36, "Vileplume"),
    "Cacnea": (32, "Cacturne"),
    "Poochyena": (18, "Mightyena"),
    "Zigzagoon": (20, "Linoone"),
    "Wurmple": (7, "Silcoon"),
    "Silcoon": (10, "Beautifly"),
    "Cascoon": (10, "Dustox"),
    "Ralts": (20, "Kirlia"),
    "Kirlia": (30, "Gardevoir"),
    "Surskit": (22, "Masquerain"),
    "Nincada": (20, "Ninjask"),
    "Whismur": (20, "Loudred"),
    "Loudred": (40, "Exploud"),
    "Makuhita": (24, "Hariyama"),
    "Azurill": (18, "Marill"),
    "Marill": (18, "Azumarill"),
    "Nosepass": (38, "Probopass"),
    "Skitty": (30, "Delcatty"),
    "Aron": (32, "Lairon"),
    "Lairon": (42, "Aggron"),
    "Meditite": (37, "Medicham"),
    "Electrike": (26, "Manectric"),
    "Numel": (33, "Camerupt"),
    "Spoink": (32, "Grumpig"),
    "Trapinch": (35, "Vibrava"),
    "Vibrava": (45, "Flygon"),
    "Spheal": (32, "Sealeo"),
    "Sealeo": (44, "Walrein"),
    "Horsea": (32, "Seadra"),
    "Seadra": (55, "Kingdra"),
    "Snorunt": (42, "Glalie"),
    "Clamperl": (32, "Huntail"),
    "Feebas": (20, "Milotic"),
}


class Pokemon:
    def __init__(self, name, hp, type, critType, moves, imgPath, level=5, experience=0):
        self.name = name
        self.hp = hp
        self.MAXhp = hp
        self.base_hp = hp
        self.type = type
        self.critType = critType
        self.moves = moves
        self.img = imgPath
        self.level = level
        self.experience = experience

    def takeDamage(self, move):
        multi = 1
        if move.type == self.critType:
            multi = 2
        self.hp -= move.damage * multi

    def xp_to_next_level(self):
        return 50 + (self.level * 10)

    def gain_experience(self, amount):
        self.experience += amount
        levels_gained = 0
        evolved = []
        while self.experience >= self.xp_to_next_level():
            self.experience -= self.xp_to_next_level()
            self.level += 1
            levels_gained += 1
            self.scale_stats_on_level_up()
            evolution_result = self.try_evolve()
            if evolution_result:
                evolved.append(evolution_result)
        return levels_gained, evolved

    def scale_stats_on_level_up(self):
        self.MAXhp += 3
        self.hp = self.MAXhp

    def try_evolve(self):
        if self.name not in EVOLUTION_LEVELS:
            return None
        required_level, evolved_name = EVOLUTION_LEVELS[self.name]
        if self.level >= required_level:
            old_name = self.name
            self.name = evolved_name
            self.MAXhp = max(self.MAXhp, self.base_hp + self.level * 2)
            self.hp = self.MAXhp
            return old_name, evolved_name, self.level
        return None
