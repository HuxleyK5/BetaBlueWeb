"""Evolution eligibility and mutation for every supported method."""

from dataclasses import dataclass

from .pokemon_data import DATABASE


@dataclass(frozen=True)
class EvolutionResult:
    success: bool
    message: str
    old_species: str | None = None
    new_species: str | None = None


class EvolutionService:
    def available(self, pokemon, trigger="level", item_id=None):
        for evolution in pokemon.species.evolutions:
            if evolution.method != trigger:
                continue
            if trigger == "level" and pokemon.level < evolution.level:
                continue
            if trigger == "item" and evolution.item != item_id:
                continue
            if trigger == "friendship" and pokemon.friendship < evolution.friendship:
                continue
            if not self._condition_matches(pokemon, evolution.condition):
                continue
            return evolution
        return None

    def evolve(self, pokemon, trigger="level", item_id=None):
        evolution = self.available(pokemon, trigger, item_id)
        if evolution is None:
            return EvolutionResult(False, f"{pokemon.display_name} cannot evolve this way.")
        old = pokemon.species
        old_hp, old_max = pokemon.current_hp, pokemon.max_hp
        pokemon.species = DATABASE.get_species(evolution.target)
        pokemon.ability = pokemon.species.abilities[0]
        pokemon.current_hp = 0 if old_hp == 0 else max(1, round(old_hp / old_max * pokemon.max_hp))
        for learned in pokemon.species.learnset:
            if learned.level <= pokemon.level and learned.move not in pokemon.known_moves:
                pokemon.known_moves.append(learned.move)
        pokemon.known_moves = pokemon.known_moves[-4:]
        return EvolutionResult(True, f"{old.name} evolved into {pokemon.species.name}!", old.key, pokemon.species.key)

    @staticmethod
    def _condition_matches(pokemon, condition):
        if not condition:
            return True
        if condition == "personality_low":
            return pokemon.personality < 128
        if condition == "personality_high":
            return pokemon.personality >= 128
        if condition == "day":
            return True
        return False
