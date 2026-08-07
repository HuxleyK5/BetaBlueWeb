"""Pokemon species, moves, and battle stats for Beta Blue."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Move:
    name: str
    power: int
    accuracy: int
    type_name: str = "Normal"
    priority: int = 0
    effect: str = ""


@dataclass
class Species:
    species_id: int
    name: str
    types: List[str]
    base_stats: Dict[str, int]
    abilities: List[str]
    catch_rate: int
    growth_rate: str
    sprite_name: str
    moves: List[Move] = field(default_factory=list)
    evolution: Dict[str, str] = field(default_factory=dict)


@dataclass
class Pokemon:
    species: Species
    level: int
    current_hp: int = 0
    experience: int = 0
    status: str = "healthy"

    def __post_init__(self):
        if self.current_hp == 0:
            self.current_hp = self.max_hp

    @property
    def max_hp(self):
        base = self.species.base_stats.get("hp", 10)
        return max(1, int((base * 2 * self.level) / 100 + self.level + 10))

    @property
    def attack(self):
        base = self.species.base_stats.get("attack", 5)
        return max(1, int((base * 2 * self.level) / 100 + 5))

    @property
    def defense(self):
        base = self.species.base_stats.get("defense", 5)
        return max(1, int((base * 2 * self.level) / 100 + 5))

    @property
    def speed(self):
        base = self.species.base_stats.get("speed", 5)
        return max(1, int((base * 2 * self.level) / 100 + 5))

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level += 1

    @property
    def experience_to_next_level(self):
        return 10 + self.level * 6


MOVE_DATABASE = {
    "Tackle": Move(name="Tackle", power=40, accuracy=100),
    "Vine Whip": Move(name="Vine Whip", power=45, accuracy=100, type_name="Grass"),
    "Ember": Move(name="Ember", power=40, accuracy=100, type_name="Fire"),
    "Water Gun": Move(name="Water Gun", power=40, accuracy=100, type_name="Water"),
    "Quick Attack": Move(name="Quick Attack", power=40, accuracy=100, priority=1),
    "Scratch": Move(name="Scratch", power=40, accuracy=100),
}

SPECIES_DATABASE = {
    "treecko": Species(
        species_id=252,
        name="Treecko",
        types=["Grass"],
        base_stats={"hp": 40, "attack": 45, "defense": 35, "speed": 70},
        abilities=["Overgrow"],
        catch_rate=45,
        growth_rate="Medium Slow",
        sprite_name="treecko",
        moves=[MOVE_DATABASE["Tackle"], MOVE_DATABASE["Quick Attack"], MOVE_DATABASE["Vine Whip"]],
        evolution={"level": 16, "into": "grovyle"},
    ),
    "torchic": Species(
        species_id=255,
        name="Torchic",
        types=["Fire"],
        base_stats={"hp": 45, "attack": 60, "defense": 40, "speed": 45},
        abilities=["Blaze"],
        catch_rate=45,
        growth_rate="Medium Slow",
        sprite_name="torchic",
        moves=[MOVE_DATABASE["Scratch"], MOVE_DATABASE["Ember"], MOVE_DATABASE["Quick Attack"]],
        evolution={"level": 16, "into": "combusken"},
    ),
    "mudkip": Species(
        species_id=258,
        name="Mudkip",
        types=["Water"],
        base_stats={"hp": 50, "attack": 70, "defense": 50, "speed": 40},
        abilities=["Torrent"],
        catch_rate=45,
        growth_rate="Medium Slow",
        sprite_name="mudkip",
        moves=[MOVE_DATABASE["Tackle"], MOVE_DATABASE["Water Gun"], MOVE_DATABASE["Mud-Slap" if "Mud-Slap" in MOVE_DATABASE else "Tackle"]],
        evolution={"level": 16, "into": "marshtomp"},
    ),
}


def create_pokemon(species_key: str, level: int = 5):
    species = SPECIES_DATABASE.get(species_key)
    if not species:
        raise ValueError(f"Unknown species: {species_key}")
    return Pokemon(species=species, level=level, current_hp=0, experience=0)
