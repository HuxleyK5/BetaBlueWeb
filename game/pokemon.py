"""Domain models for species definitions and individual Pokemon."""

from dataclasses import dataclass, field
from typing import Optional
import random


STAT_NAMES = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")
VALID_TYPES = {
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison",
    "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy",
}
VALID_GROWTH_RATES = {"fast", "medium_fast", "medium_slow", "slow", "erratic", "fluctuating"}


@dataclass(frozen=True)
class BaseStats:
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    def __getitem__(self, stat_name):
        if stat_name not in STAT_NAMES:
            raise KeyError(stat_name)
        return getattr(self, stat_name)

    def get(self, stat_name, default=None):
        return getattr(self, stat_name, default)


@dataclass(frozen=True)
class Move:
    key: str
    name: str
    type_name: str
    category: str
    power: int
    accuracy: int
    pp: int
    priority: int = 0
    effect: str = ""


@dataclass(frozen=True)
class LearnedMove:
    level: int
    move: Move


@dataclass(frozen=True)
class Evolution:
    target: str
    method: str
    level: Optional[int] = None
    item: Optional[str] = None
    friendship: Optional[int] = None
    condition: Optional[str] = None


@dataclass(frozen=True)
class Species:
    key: str
    species_id: int
    name: str
    types: tuple[str, ...]
    abilities: tuple[str, ...]
    base_stats: BaseStats
    learnset: tuple[LearnedMove, ...]
    evolutions: tuple[Evolution, ...]
    sprite_path: str
    catch_rate: int
    growth_rate: str
    egg_groups: tuple[str, ...] = ("field",)
    hatch_steps: int = 512

    @property
    def moves(self):
        """Compatibility view used by the current prototype battle module."""
        return tuple(entry.move for entry in self.learnset)

    @property
    def sprite_name(self):
        return self.key


@dataclass
class Pokemon:
    """A mutable individual that references an immutable species definition."""

    species: Species
    level: int
    current_hp: int = 0
    experience: int = 0
    status: str = "healthy"
    nickname: Optional[str] = None
    ability: Optional[str] = None
    known_moves: list[Move] = field(default_factory=list)
    friendship: int = 70
    personality: int = field(default_factory=lambda: random.randrange(256))
    gender: str = field(default_factory=lambda: random.choice(("male", "female")))

    def __post_init__(self):
        if not 1 <= self.level <= 100:
            raise ValueError("Pokemon level must be between 1 and 100")
        self.friendship = max(0, min(255, self.friendship))
        if self.gender not in {"male", "female", "genderless"}:
            raise ValueError("Pokemon gender must be male, female, or genderless")
        if self.ability is None:
            self.ability = self.species.abilities[0]
        if self.ability not in self.species.abilities:
            raise ValueError(f"{self.ability} is not an ability for {self.species.name}")
        if not self.known_moves:
            available = [entry.move for entry in self.species.learnset if entry.level <= self.level]
            self.known_moves = available[-4:]
        if self.current_hp <= 0:
            self.current_hp = self.max_hp
        self.current_hp = min(self.current_hp, self.max_hp)

    @property
    def display_name(self):
        return self.nickname or self.species.name

    def stat(self, name):
        base = self.species.base_stats[name]
        if name == "hp":
            return max(1, (2 * base * self.level) // 100 + self.level + 10)
        return max(1, (2 * base * self.level) // 100 + 5)

    @property
    def max_hp(self):
        return self.stat("hp")

    @property
    def attack(self):
        return self.stat("attack")

    @property
    def defense(self):
        return self.stat("defense")

    @property
    def special_attack(self):
        return self.stat("special_attack")

    @property
    def special_defense(self):
        return self.stat("special_defense")

    @property
    def speed(self):
        return self.stat("speed")

    @property
    def experience_to_next_level(self):
        if self.level >= 100:
            return 0
        return max(1, _total_experience(self.level + 1, self.species.growth_rate) - _total_experience(self.level, self.species.growth_rate))

    def gain_experience(self, amount):
        if amount < 0:
            raise ValueError("Experience gain cannot be negative")
        levels_gained = 0
        self.experience += amount
        while self.level < 100 and self.experience >= self.experience_to_next_level:
            old_max_hp = self.max_hp
            self.experience -= self.experience_to_next_level
            self.level += 1
            self.current_hp += self.max_hp - old_max_hp
            levels_gained += 1
            self._learn_level_moves()
        return levels_gained

    def gain_friendship(self, amount):
        old = self.friendship
        self.friendship = max(0, min(255, self.friendship + amount))
        return self.friendship - old

    def to_dict(self):
        """Return lifecycle state in a Phase 12-compatible shape."""
        return {
            "species": self.species.key, "level": self.level, "current_hp": self.current_hp,
            "experience": self.experience, "status": self.status, "nickname": self.nickname,
            "ability": self.ability, "moves": [move.key for move in self.known_moves],
            "friendship": self.friendship, "personality": self.personality, "gender": self.gender,
        }

    def _learn_level_moves(self):
        for entry in self.species.learnset:
            if entry.level == self.level and entry.move not in self.known_moves:
                self.known_moves.append(entry.move)
        self.known_moves = self.known_moves[-4:]


def _total_experience(level, growth_rate):
    """Return total experience at a level using expandable growth groups."""
    if growth_rate == "fast":
        return 4 * level ** 3 // 5
    if growth_rate == "slow":
        return 5 * level ** 3 // 4
    if growth_rate == "medium_slow":
        return max(0, 6 * level ** 3 // 5 - 15 * level ** 2 + 100 * level - 140)
    # Medium-fast is also the stable fallback for future custom growth groups.
    return level ** 3
