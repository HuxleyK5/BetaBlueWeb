"""Wild encounter system with zone definitions and spawn rates."""

import random
from dataclasses import dataclass
from typing import List, Dict

from .pokemon_data import create_pokemon
from .map import TILE_GRASS, TILE_WATER


@dataclass
class EncounterEntry:
    species_key: str
    weight: int
    min_level: int
    max_level: int


@dataclass
class EncounterZone:
    tile_types: List[int]
    entries: List[EncounterEntry]
    encounter_rate: float

    def choose_pokemon(self):
        pool = []
        for entry in self.entries:
            pool.extend([entry] * entry.weight)
        if not pool:
            return None
        choice = random.choice(pool)
        level = random.randint(choice.min_level, choice.max_level)
        return create_pokemon(choice.species_key, level)

    def should_encounter(self):
        return random.random() < self.encounter_rate


GRASS_ENCOUNTERS = EncounterZone(
    tile_types=[TILE_GRASS],
    entries=[
        EncounterEntry("treecko", 30, 5, 7),
        EncounterEntry("torchic", 25, 5, 7),
        EncounterEntry("mudkip", 20, 5, 7),
    ],
    encounter_rate=0.08,
)

WATER_ENCOUNTERS = EncounterZone(
    tile_types=[TILE_WATER],
    entries=[
        EncounterEntry("mudkip", 40, 5, 7),
        EncounterEntry("treecko", 30, 5, 6),
    ],
    encounter_rate=0.06,
)


def get_encounter_for_tile(tile_type):
    if tile_type == TILE_WATER:
        return WATER_ENCOUNTERS
    return GRASS_ENCOUNTERS


def try_trigger_encounter(tile_type):
    zone = get_encounter_for_tile(tile_type)
    if zone and zone.should_encounter():
        return zone.choose_pokemon()
    return None
