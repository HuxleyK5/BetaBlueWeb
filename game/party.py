"""Party and Pokemon storage management."""

from typing import List
from .pokemon_data import Pokemon


class PartyManager:
    def __init__(self, max_party_size: int = 6):
        self.max_party_size = max_party_size
        self.party: List[Pokemon] = []
        self.boxes: List[List[Pokemon]] = [[]]
        self.active_index = 0

    @property
    def active_pokemon(self):
        if 0 <= self.active_index < len(self.party):
            return self.party[self.active_index]
        return None

    def add_pokemon(self, pokemon: Pokemon):
        if len(self.party) < self.max_party_size:
            self.party.append(pokemon)
            return True
        self.boxes[0].append(pokemon)
        return False

    def swap_party(self, index_a: int, index_b: int):
        if 0 <= index_a < len(self.party) and 0 <= index_b < len(self.party):
            self.party[index_a], self.party[index_b] = self.party[index_b], self.party[index_a]
            if self.active_index == index_a:
                self.active_index = index_b
            elif self.active_index == index_b:
                self.active_index = index_a

    def has_usable_pokemon(self):
        return any(p.current_hp > 0 for p in self.party)

    def heal_all(self):
        for pokemon in self.party:
            pokemon.current_hp = pokemon.max_hp

    def get_party_summary(self):
        return [f"{p.species.name} Lv{p.level} HP{p.current_hp}/{p.max_hp}" for p in self.party]
