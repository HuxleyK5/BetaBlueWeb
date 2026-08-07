"""Persistence and save/load functionality."""

import json
from pathlib import Path

from .pokemon_data import Pokemon
from .items import Inventory
from .pokedex import Pokedex


SAVE_FILENAME = "savegame.json"


def save_game(root_path, player_name, player_position, pokemon_party, inventory: Inventory, pokedex: Pokedex):
    data = {
        "player_name": player_name,
        "player_position": player_position,
        "party": [
            {
                "species_key": pokemon.species.name.lower(),
                "level": pokemon.level,
                "current_hp": pokemon.current_hp,
                "experience": pokemon.experience,
            }
            for pokemon in pokemon_party
        ],
        "inventory": inventory.items,
        "pokedex": list(pokedex.discovered),
    }
    path = Path(root_path) / SAVE_FILENAME
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_game(root_path, pokemon_factory, inventory: Inventory, pokedex: Pokedex):
    path = Path(root_path) / SAVE_FILENAME
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    inventory.items = data.get("inventory", {})
    pokedex.discovered = set(data.get("pokedex", []))
    party = []
    for entry in data.get("party", []):
        pokemon = pokemon_factory(entry["species_key"], entry["level"])
        pokemon.current_hp = entry.get("current_hp", pokemon.max_hp)
        pokemon.experience = entry.get("experience", 0)
        party.append(pokemon)
    return {
        "player_name": data.get("player_name", ""),
        "player_position": data.get("player_position", (10, 7)),
        "party": party,
    }
