"""Nursery, breeding compatibility, Eggs, and step-based hatching."""

from dataclasses import dataclass

from .pokemon_data import DATABASE


@dataclass
class Egg:
    species_key: str
    steps_required: int
    steps_walked: int = 0
    inherited_move: str | None = None

    @property
    def ready(self):
        return self.steps_walked >= self.steps_required

    @property
    def remaining_steps(self):
        return max(0, self.steps_required - self.steps_walked)

    def to_dict(self):
        return {"species": self.species_key, "steps_required": self.steps_required, "steps_walked": self.steps_walked, "inherited_move": self.inherited_move}


class Nursery:
    def __init__(self, max_eggs=6):
        self.eggs = []
        self.max_eggs = max_eggs

    @staticmethod
    def compatible(parent_a, parent_b):
        if parent_a is parent_b or "undiscovered" in parent_a.species.egg_groups or "undiscovered" in parent_b.species.egg_groups:
            return False
        shared = set(parent_a.species.egg_groups) & set(parent_b.species.egg_groups)
        return bool(shared) and parent_a.gender != parent_b.gender and "genderless" not in {parent_a.gender, parent_b.gender}

    def breed(self, parent_a, parent_b):
        if len(self.eggs) >= self.max_eggs:
            return None, "The Nursery is already caring for too many Eggs."
        if not self.compatible(parent_a, parent_b):
            return None, "Those Pokemon are not compatible breeding partners."
        mother = parent_a if parent_a.gender == "female" else parent_b
        baby_key = self._family_base(mother.species.key)
        baby = DATABASE.get_species(baby_key)
        shared_moves = {move.key for move in parent_a.known_moves} & {move.key for move in parent_b.known_moves}
        egg = Egg(baby.key, baby.hatch_steps, inherited_move=next(iter(sorted(shared_moves)), None))
        self.eggs.append(egg)
        return egg, f"The Nursery discovered a {baby.name} Egg!"

    def advance_steps(self, steps=1):
        newly_ready = []
        for egg in self.eggs:
            was_ready = egg.ready
            egg.steps_walked += max(0, steps)
            if egg.ready and not was_ready:
                newly_ready.append(egg)
        return newly_ready

    def hatch_ready(self, party):
        hatched = []
        for egg in list(self.eggs):
            if not egg.ready:
                continue
            pokemon = DATABASE.create_pokemon(egg.species_key, 1, friendship=120)
            if egg.inherited_move and DATABASE.get_move(egg.inherited_move) not in pokemon.known_moves:
                pokemon.known_moves.append(DATABASE.get_move(egg.inherited_move))
                pokemon.known_moves = pokemon.known_moves[-4:]
            if not party.add_pokemon(pokemon):
                continue
            self.eggs.remove(egg)
            hatched.append(pokemon)
        return hatched

    @staticmethod
    def _family_base(species_key):
        for candidate in DATABASE.species.values():
            if any(evolution.target == species_key for evolution in candidate.evolutions):
                return Nursery._family_base(candidate.key)
        return species_key

    def to_dict(self):
        return [egg.to_dict() for egg in self.eggs]
