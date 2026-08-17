"""Compatibility facade for the data-driven Pokémon system.

New code may import domain models from ``game.pokemon`` and use
``PokemonDatabase`` directly. Existing systems can keep importing this module.
"""

from .pokemon import BaseStats, Evolution, LearnedMove, Move, Pokemon, Species
from .pokemon_database import PokemonDataError, PokemonDatabase


DATABASE = PokemonDatabase()
MOVE_DATABASE = DATABASE.moves
SPECIES_DATABASE = DATABASE.species


def create_pokemon(species_key, level=5, **kwargs):
    return DATABASE.create_pokemon(species_key, level, **kwargs)


__all__ = [
    "BaseStats", "DATABASE", "Evolution", "LearnedMove", "MOVE_DATABASE", "Move",
    "Pokemon", "PokemonDataError", "PokemonDatabase", "SPECIES_DATABASE", "Species",
    "create_pokemon",
]
