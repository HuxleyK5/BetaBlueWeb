"""Terrain-aware, weighted wild encounter selection."""

from dataclasses import dataclass
import json
from pathlib import Path
import random

from .config import PROJECT_ROOT
from .map import TILE_CAVE, TILE_TALL_GRASS, TILE_WATER
from .pokemon_data import DATABASE


RARITIES = {"common", "uncommon", "rare", "legendary"}
ZONE_BY_TILE = {TILE_TALL_GRASS: "grass", TILE_WATER: "water", TILE_CAVE: "cave"}


@dataclass(frozen=True)
class EncounterContext:
    """Environmental filters prepared for the Phase 13 world simulation."""

    weather: str = "clear"
    season: str = "summer"
    time_of_day: str = "day"


@dataclass(frozen=True)
class EncounterEntry:
    species_key: str
    weight: int
    min_level: int
    max_level: int
    rarity: str
    conditions: dict[str, object]
    legendary_event: bool = False

    def matches(self, context):
        for name, required in self.conditions.items():
            actual = getattr(context, name, None)
            options = required if isinstance(required, list) else [required]
            if actual not in options:
                return False
        return True


@dataclass(frozen=True)
class EncounterTable:
    area_id: str
    zone: str
    encounter_rate: float
    entries: tuple[EncounterEntry, ...]


@dataclass(frozen=True)
class WildEncounter:
    pokemon: object
    rarity: str
    zone: str
    legendary_event: bool = False


class EncounterDataError(ValueError):
    """Raised when an encounter table cannot be loaded safely."""


class EncounterManager:
    def __init__(self, data_path=None, rng=None, grace_steps=4):
        self.data_path = Path(data_path or PROJECT_ROOT / "Pokemon" / "data" / "encounters.json")
        self.rng = rng or random.Random()
        self.grace_steps = grace_steps
        self.steps_since_reset = 0
        self.tables = self._load_tables()

    def reset_grace(self):
        self.steps_since_reset = 0

    def validate_areas(self, area_ids):
        unknown = sorted({area for area, _zone in self.tables if area != "*" and area not in area_ids})
        if unknown:
            raise EncounterDataError(f"Encounter tables reference unknown areas: {', '.join(unknown)}")

    def table_for(self, area_id, tile_symbol):
        zone = ZONE_BY_TILE.get(tile_symbol)
        if zone is None:
            return None
        return self.tables.get((area_id, zone)) or self.tables.get(("*", zone))

    def roll(self, area_id, tile_symbol, context=None):
        """Roll once after a completed eligible step and return a wild Pokémon."""
        table = self.table_for(area_id, tile_symbol)
        if table is None:
            return None
        self.steps_since_reset += 1
        if self.steps_since_reset <= self.grace_steps or self.rng.random() >= table.encounter_rate:
            return None

        context = context or EncounterContext()
        eligible = [entry for entry in table.entries if entry.matches(context)]
        if not eligible:
            return None
        entry = self.rng.choices(eligible, weights=[item.weight for item in eligible], k=1)[0]
        level = self.rng.randint(entry.min_level, entry.max_level)
        self.reset_grace()
        return WildEncounter(DATABASE.create_pokemon(entry.species_key, level), entry.rarity, table.zone, entry.legendary_event)

    def _load_tables(self):
        try:
            raw_tables = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise EncounterDataError(f"Could not load {self.data_path.name}: {error}") from error
        if not isinstance(raw_tables, list):
            raise EncounterDataError("Encounter data must contain a JSON list")

        tables = {}
        for raw in raw_tables:
            try:
                key = (raw["area"], raw["zone"])
                entries = tuple(
                    EncounterEntry(
                        item["species"], item["weight"], item["min_level"], item["max_level"],
                        item["rarity"], item.get("conditions", {}), item.get("legendary_event", False),
                    )
                    for item in raw["entries"]
                )
                table = EncounterTable(raw["area"], raw["zone"], raw["encounter_rate"], entries)
            except (KeyError, TypeError) as error:
                raise EncounterDataError(f"Invalid encounter table: {raw}") from error
            if key in tables:
                raise EncounterDataError(f"Duplicate encounter table for {key}")
            self._validate_table(table)
            tables[key] = table
        return tables

    @staticmethod
    def _validate_table(table):
        if table.zone not in set(ZONE_BY_TILE.values()):
            raise EncounterDataError(f"Unknown encounter zone '{table.zone}'")
        if not isinstance(table.encounter_rate, (int, float)) or isinstance(table.encounter_rate, bool) or not 0 <= table.encounter_rate <= 1:
            raise EncounterDataError(f"Invalid encounter rate for {table.area_id}/{table.zone}")
        if not table.entries:
            raise EncounterDataError(f"Empty encounter table for {table.area_id}/{table.zone}")
        allowed_conditions = set(EncounterContext.__dataclass_fields__)
        for entry in table.entries:
            if entry.species_key not in DATABASE.species:
                raise EncounterDataError(f"Unknown encounter species '{entry.species_key}'")
            numeric = (entry.weight, entry.min_level, entry.max_level)
            if any(not isinstance(value, int) or isinstance(value, bool) for value in numeric):
                raise EncounterDataError(f"Encounter values for '{entry.species_key}' must be integers")
            if entry.weight <= 0 or not 1 <= entry.min_level <= entry.max_level <= 100:
                raise EncounterDataError(f"Invalid weight or levels for '{entry.species_key}'")
            if entry.rarity not in RARITIES:
                raise EncounterDataError(f"Invalid rarity '{entry.rarity}'")
            if not isinstance(entry.conditions, dict) or not set(entry.conditions).issubset(allowed_conditions):
                raise EncounterDataError(f"Invalid conditions for '{entry.species_key}'")
            if not isinstance(entry.legendary_event, bool):
                raise EncounterDataError(f"Legendary event flag for '{entry.species_key}' must be boolean")
