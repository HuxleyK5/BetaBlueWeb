"""Six-member party management and capacity-limited Pokémon storage boxes."""

from dataclasses import dataclass, field

from .pokemon_data import Pokemon


@dataclass
class StorageBox:
    name: str
    capacity: int = 30
    pokemon: list[Pokemon] = field(default_factory=list)

    @property
    def is_full(self):
        return len(self.pokemon) >= self.capacity

    def deposit(self, pokemon):
        if self.is_full:
            return False
        self.pokemon.append(pokemon)
        return True


class PokemonStorage:
    def __init__(self, box_count=8, box_capacity=30):
        self.boxes = [StorageBox(f"Box {index + 1}", box_capacity) for index in range(box_count)]

    def deposit(self, pokemon):
        for box_index, box in enumerate(self.boxes):
            if box.deposit(pokemon):
                return box_index, len(box.pokemon) - 1
        return None

    def withdraw(self, box_index, slot_index):
        if not 0 <= box_index < len(self.boxes):
            return None
        box = self.boxes[box_index]
        if not 0 <= slot_index < len(box.pokemon):
            return None
        return box.pokemon.pop(slot_index)


class PartyManager:
    def __init__(self, max_party_size=6, storage=None):
        self.max_party_size = max_party_size
        self.party: list[Pokemon] = []
        self.storage = storage or PokemonStorage()
        self.active_index = 0
        self.last_placement = None

    @property
    def boxes(self):
        """Compatibility view for code that previously accessed nested lists."""
        return [box.pokemon for box in self.storage.boxes]

    @property
    def active_pokemon(self):
        if 0 <= self.active_index < len(self.party):
            return self.party[self.active_index]
        return None

    def add_pokemon(self, pokemon):
        if len(self.party) < self.max_party_size:
            self.party.append(pokemon)
            self.last_placement = ("party", len(self.party) - 1)
            return True
        location = self.storage.deposit(pokemon)
        self.last_placement = ("storage", *location) if location is not None else None
        return location is not None

    def has_capture_capacity(self):
        return len(self.party) < self.max_party_size or any(not box.is_full for box in self.storage.boxes)

    def deposit_party_member(self, party_index, box_index=0):
        if len(self.party) <= 1 or not 0 <= party_index < len(self.party):
            return False
        if not 0 <= box_index < len(self.storage.boxes):
            return False
        pokemon = self.party[party_index]
        if not self.storage.boxes[box_index].deposit(pokemon):
            return False
        self.party.pop(party_index)
        self.active_index = min(self.active_index, len(self.party) - 1)
        return True

    def withdraw_to_party(self, box_index, slot_index):
        if len(self.party) >= self.max_party_size:
            return False
        pokemon = self.storage.withdraw(box_index, slot_index)
        if pokemon is None:
            return False
        self.party.append(pokemon)
        return True

    def swap_party(self, index_a, index_b):
        if 0 <= index_a < len(self.party) and 0 <= index_b < len(self.party):
            self.party[index_a], self.party[index_b] = self.party[index_b], self.party[index_a]
            if self.active_index == index_a:
                self.active_index = index_b
            elif self.active_index == index_b:
                self.active_index = index_a

    def has_usable_pokemon(self):
        return any(pokemon.current_hp > 0 for pokemon in self.party)

    def heal_all(self):
        for pokemon in self.party:
            pokemon.current_hp = pokemon.max_hp

    def get_party_summary(self):
        return [f"{pokemon.species.name} Lv{pokemon.level} HP{pokemon.current_hp}/{pokemon.max_hp}" for pokemon in self.party]
