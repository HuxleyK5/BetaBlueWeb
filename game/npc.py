"""NPCs, trainers, and interaction logic."""

from dataclasses import dataclass, field
from typing import List

from .pokemon_data import Pokemon


@dataclass
class NPC:
    name: str
    tile_x: int
    tile_y: int
    dialogue: List[str]
    is_trainer: bool = False
    party: List[Pokemon] = field(default_factory=list)
    has_battled: bool = False
    schedule: List[tuple] = field(default_factory=list)

    def interact(self):
        return self.dialogue

    def can_battle(self):
        return self.is_trainer and not self.has_battled and len(self.party) > 0
