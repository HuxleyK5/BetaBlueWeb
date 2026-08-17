"""Validated JSON loader and indexes for Pokemon and move definitions."""

import json
from pathlib import Path
from .items import ITEM_DATABASE

from .config import PROJECT_ROOT
from .pokemon import (
    BaseStats, Evolution, LearnedMove, Move, Pokemon, Species, STAT_NAMES,
    VALID_GROWTH_RATES, VALID_TYPES,
)


class PokemonDataError(ValueError):
    """Raised when Pokémon data is malformed or references missing records."""


class PokemonDatabase:
    def __init__(self, data_path=None, validate_sprites=True):
        self.data_path = Path(data_path or PROJECT_ROOT / "pokemon" / "data")
        self.validate_sprites = validate_sprites
        self.moves = self._load_moves(self.data_path / "moves.json")
        self.species = self._load_species(self.data_path / "species.json")
        self.species_by_id = {entry.species_id: entry for entry in self.species.values()}
        self._validate_cross_references()

    def get_species(self, key_or_id):
        species = self.species_by_id.get(key_or_id) if isinstance(key_or_id, int) else self.species.get(str(key_or_id).lower())
        if species is None:
            raise KeyError(f"Unknown species: {key_or_id}")
        return species

    def get_move(self, key):
        try:
            return self.moves[str(key).lower()]
        except KeyError as error:
            raise KeyError(f"Unknown move: {key}") from error

    def create_pokemon(self, species_key, level=5, **kwargs):
        return Pokemon(self.get_species(species_key), level, **kwargs)

    @staticmethod
    def _read_json(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise PokemonDataError(f"Could not load {path.name}: {error}") from error
        if not isinstance(data, list):
            raise PokemonDataError(f"{path.name} must contain a JSON list")
        return data

    def _load_moves(self, path):
        moves = {}
        for raw in self._read_json(path):
            try:
                move = Move(
                    key=raw["key"].lower(), name=raw["name"], type_name=raw["type"],
                    category=raw["category"], power=raw["power"], accuracy=raw["accuracy"],
                    pp=raw["pp"], priority=raw.get("priority", 0), effect=raw.get("effect", ""),
                )
            except (KeyError, TypeError, AttributeError) as error:
                raise PokemonDataError(f"Invalid move record: {raw}") from error
            if move.key in moves:
                raise PokemonDataError(f"Duplicate move key '{move.key}'")
            if move.type_name not in VALID_TYPES or move.category not in {"physical", "special", "status"}:
                raise PokemonDataError(f"Move '{move.key}' has an invalid type or category")
            numeric_values = (move.power, move.accuracy, move.pp, move.priority)
            if any(not isinstance(value, int) or isinstance(value, bool) for value in numeric_values):
                raise PokemonDataError(f"Move '{move.key}' battle values must be integers")
            if not 0 <= move.power <= 300 or not 1 <= move.accuracy <= 100 or move.pp <= 0:
                raise PokemonDataError(f"Move '{move.key}' has invalid battle values")
            moves[move.key] = move
        return moves

    def _load_species(self, path):
        species = {}
        ids = set()
        for raw in self._read_json(path):
            try:
                key = raw["key"].lower()
                stats = BaseStats(**raw["base_stats"])
                learnset = tuple(LearnedMove(item["level"], self.moves[item["move"]]) for item in raw["moves"])
                evolutions = tuple(Evolution(**item) for item in raw.get("evolutions", []))
                entry = Species(
                    key, raw["id"], raw["name"], tuple(raw["types"]), tuple(raw["abilities"]),
                    stats, learnset, evolutions, raw["sprite"], raw["catch_rate"], raw["growth_rate"],
                    tuple(raw.get("egg_groups", [raw["types"][0].lower()])), raw.get("hatch_steps", 512),
                )
            except (KeyError, TypeError, AttributeError) as error:
                raise PokemonDataError(f"Invalid species record: {raw.get('key', raw)}") from error
            if key in species or entry.species_id in ids:
                raise PokemonDataError(f"Duplicate species key or ID for '{key}'")
            if any(not isinstance(value, int) or isinstance(value, bool) for value in (entry.species_id, entry.catch_rate)):
                raise PokemonDataError(f"Species '{key}' ID and catch rate must be integers")
            if not 1 <= entry.species_id or not 1 <= entry.catch_rate <= 255:
                raise PokemonDataError(f"Species '{key}' has an invalid ID or catch rate")
            if not 1 <= len(entry.types) <= 2 or any(value not in VALID_TYPES for value in entry.types):
                raise PokemonDataError(f"Species '{key}' has invalid types")
            if not entry.abilities or entry.growth_rate not in VALID_GROWTH_RATES:
                raise PokemonDataError(f"Species '{key}' has invalid abilities or growth rate")
            if not entry.egg_groups or not all(isinstance(group, str) and group for group in entry.egg_groups):
                raise PokemonDataError(f"Species '{key}' has invalid egg groups")
            if not isinstance(entry.hatch_steps, int) or isinstance(entry.hatch_steps, bool) or entry.hatch_steps <= 0:
                raise PokemonDataError(f"Species '{key}' has invalid hatch steps")
            if any(not isinstance(stats[name], int) or isinstance(stats[name], bool) for name in STAT_NAMES):
                raise PokemonDataError(f"Species '{key}' base stats must be integers")
            if any(stats[name] <= 0 or stats[name] > 255 for name in STAT_NAMES):
                raise PokemonDataError(f"Species '{key}' has invalid base stats")
            if any(not isinstance(item.level, int) or isinstance(item.level, bool) for item in learnset):
                raise PokemonDataError(f"Species '{key}' learnset levels must be integers")
            if any(item.level < 1 or item.level > 100 for item in learnset):
                raise PokemonDataError(f"Species '{key}' has an invalid learnset level")
            species[key] = entry
            ids.add(entry.species_id)
        return species

    def _validate_cross_references(self):
        valid_methods = {"level", "item", "trade", "friendship"}
        for species in self.species.values():
            sprite_path = (PROJECT_ROOT / species.sprite_path).resolve()
            if not sprite_path.is_relative_to(PROJECT_ROOT.resolve()):
                raise PokemonDataError(f"Sprite for '{species.key}' must remain inside the project")
            if self.validate_sprites and not sprite_path.is_file():
                raise PokemonDataError(f"Missing sprite for '{species.key}': {species.sprite_path}")
            for evolution in species.evolutions:
                if evolution.target not in self.species:
                    raise PokemonDataError(f"Species '{species.key}' evolves into missing species '{evolution.target}'")
                if evolution.method not in valid_methods:
                    raise PokemonDataError(f"Species '{species.key}' has invalid evolution method '{evolution.method}'")
                if evolution.method == "level" and (
                    not isinstance(evolution.level, int) or isinstance(evolution.level, bool) or not 1 <= evolution.level <= 100
                ):
                    raise PokemonDataError(f"Species '{species.key}' has a level evolution without a level")
                if evolution.method == "item" and not evolution.item:
                    raise PokemonDataError(f"Species '{species.key}' has an item evolution without an item")
                if evolution.method == "item" and evolution.item not in ITEM_DATABASE:
                    raise PokemonDataError(f"Species '{species.key}' references unknown evolution item '{evolution.item}'")
                if evolution.method == "friendship" and (
                    not isinstance(evolution.friendship, int) or isinstance(evolution.friendship, bool)
                    or not 0 <= evolution.friendship <= 255
                ):
                    raise PokemonDataError(f"Species '{species.key}' has a friendship evolution without a threshold")
