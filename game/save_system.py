"""Versioned, validated, atomic persistence for the complete game state."""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil

from .breeding import Egg
from .config import Settings
from .items import ITEM_DATABASE
from .party import PartyManager
from .pokemon_data import DATABASE
from .quests import QuestProgress
from .weather import SEASONS, WorldSimulation


SAVE_VERSION = 2
SAVE_FILENAME = "savegame.json"


class SaveError(RuntimeError):
    """A readable save/load failure that should not crash the game loop."""


class SaveManager:
    def __init__(self, saves_path):
        self.saves_path = Path(saves_path)
        self.path = self.saves_path / SAVE_FILENAME
        self.backup_path = self.saves_path / f"{SAVE_FILENAME}.bak"

    @property
    def has_save(self):
        return self.path.is_file()

    def save(self, game):
        data = self._snapshot(game)
        self.saves_path.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        try:
            with temporary.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            if self.path.exists():
                shutil.copy2(self.path, self.backup_path)
            os.replace(temporary, self.path)
        except OSError as error:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            raise SaveError(f"Could not save the game: {error}") from error
        return self.path

    def load(self, game):
        data = self._read()
        prepared = self._prepare(game, data)
        self._apply(game, prepared)
        return data.get("saved_at", "")

    def _read(self):
        if not self.has_save:
            raise SaveError("No save file exists yet.")
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise SaveError(f"The save file could not be read: {error}") from error
        if not isinstance(data, dict) or data.get("schema_version") not in {1, SAVE_VERSION}:
            raise SaveError("This save file uses an unsupported schema version.")
        if data["schema_version"] == 1:
            data = self._migrate_v1(data)
        return data

    @staticmethod
    def _migrate_v1(data):
        context = data.get("encounter_context", {})
        hours = {"dawn": 6, "day": 10, "dusk": 19, "night": 22}
        season = context.get("season", "spring")
        season_index = SEASONS.index(season) if season in SEASONS else 0
        data["world_simulation"] = {
            "total_minutes": season_index * 3 * 1440 + hours.get(context.get("time_of_day"), 10) * 60,
            "weather": "clear" if context.get("weather") == "starfall" else context.get("weather", "clear"),
            "weather_minutes_remaining": 120, "seed": 1337,
        }
        data["schema_version"] = SAVE_VERSION
        return data

    def _prepare(self, game, data):
        """Validate and reconstruct everything before mutating the live game."""
        try:
            trainer = data["trainer"]
            if not isinstance(trainer.get("name"), str) or not trainer["name"]:
                raise ValueError("invalid trainer name")
            integer_stats = ("money", "badges", "pokemon_seen", "pokemon_caught", "steps_taken")
            if any(not isinstance(trainer.get(key), int) or isinstance(trainer.get(key), bool) or trainer[key] < 0 for key in integer_stats):
                raise ValueError("invalid trainer statistics")
            if not isinstance(trainer.get("play_time_seconds"), (int, float)) or trainer["play_time_seconds"] < 0:
                raise ValueError("invalid play time")
            location = data["location"]
            if location["area"] not in game.world.areas:
                raise ValueError("unknown saved area")
            area = game.world.areas[location["area"]]
            position = tuple(location["position"])
            if len(position) != 2 or area.game_map.is_solid(*position):
                raise ValueError("invalid saved position")
            party = PartyManager()
            party.party = [self._pokemon(entry) for entry in data["party"]["members"]]
            if not 1 <= len(party.party) <= party.max_party_size:
                raise ValueError("saved party size is invalid")
            boxes = data["storage"]["boxes"]
            if len(boxes) != len(party.storage.boxes):
                raise ValueError("saved storage box count is invalid")
            for box, entries in zip(party.storage.boxes, boxes):
                if len(entries) > box.capacity:
                    raise ValueError("saved storage box exceeds capacity")
                box.pokemon = [self._pokemon(entry) for entry in entries]
            party.active_index = max(0, min(data["party"].get("active_index", 0), len(party.party) - 1))
            inventory = self._inventory(data["inventory"])
            quest_states = self._quests(game, data["quests"])
            story = data["story"]
            if not isinstance(story.get("active_chapter"), str) or not isinstance(story.get("badges"), list) or not isinstance(story.get("flags"), list):
                raise ValueError("invalid story state")
            npc_states = self._npcs(game, data["npcs"])
            eggs = self._eggs(data["nursery"])
            simulation = WorldSimulation()
            simulation.restore(data["world_simulation"])
            settings = Settings(**data.get("settings", asdict(game.settings)))
            if settings.window_width <= 0 or settings.window_height <= 0 or settings.target_fps <= 0:
                raise ValueError("invalid saved settings")
        except (KeyError, TypeError, ValueError) as error:
            raise SaveError(f"The save file contains invalid game state: {error}") from error
        return {
            "trainer": trainer, "area": area, "position": position, "direction": location.get("direction", "down"),
            "party": party, "inventory": inventory, "quests": quest_states, "story": story,
            "npcs": npc_states, "eggs": eggs, "simulation": simulation, "settings": settings,
        }

    @staticmethod
    def _pokemon(entry):
        level = entry["level"]
        if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 100:
            raise ValueError("invalid Pokemon level")
        moves = [DATABASE.get_move(key) for key in entry.get("moves", [])]
        experience = entry.get("experience", 0)
        if not isinstance(experience, int) or isinstance(experience, bool) or experience < 0:
            raise ValueError("invalid Pokemon experience")
        pokemon = DATABASE.create_pokemon(
            entry["species"], level, experience=experience,
            status=entry.get("status", "healthy"), nickname=entry.get("nickname"),
            ability=entry.get("ability"), known_moves=moves,
            friendship=entry.get("friendship", 70), personality=entry.get("personality", 0),
            gender=entry.get("gender", "genderless"),
        )
        hp = entry.get("current_hp", pokemon.max_hp)
        if not isinstance(hp, int) or isinstance(hp, bool) or not 0 <= hp <= pokemon.max_hp:
            raise ValueError("invalid Pokemon HP")
        pokemon.current_hp = hp
        return pokemon

    @staticmethod
    def _inventory(data):
        from .items import Inventory
        if not isinstance(data, dict):
            raise ValueError("invalid inventory")
        inventory = Inventory({})
        for item_id, count in data.items():
            if item_id not in ITEM_DATABASE or not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= inventory.MAX_PER_ITEM:
                raise ValueError("invalid inventory entry")
            inventory.add(item_id, count)
        return inventory

    @staticmethod
    def _quests(game, data):
        if set(data) != set(game.quests.definitions):
            raise ValueError("save quests do not match current quest content")
        result = {}
        for quest_id, raw in data.items():
            definition = game.quests.definitions[quest_id]
            expected = {obj.objective_id for obj in definition.objectives}
            if set(raw.get("objectives", {})) != expected or raw.get("status") not in {"locked", "active", "completed"}:
                raise ValueError("invalid quest progress")
            counts = raw["objectives"]
            if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in counts.values()):
                raise ValueError("invalid objective count")
            limits = {obj.objective_id: obj.required for obj in definition.objectives}
            if any(value > limits[key] for key, value in counts.items()):
                raise ValueError("objective count exceeds its requirement")
            result[quest_id] = QuestProgress(raw["status"], dict(counts), bool(raw.get("reward_claimed", False)))
        return result

    @staticmethod
    def _npcs(game, data):
        if set(data) != set(game.npcs.npcs):
            raise ValueError("save NPCs do not match current content")
        result = {}
        for npc_id, raw in data.items():
            npc = game.npcs.npcs[npc_id]
            position = tuple(raw["position"])
            area = game.world.areas[npc.area_id]
            if len(position) != 2 or area.game_map.is_solid(*position):
                raise ValueError("invalid NPC position")
            required = {"direction", "interacted", "defeated", "reward_claimed", "patrol_index", "active_schedule_index"}
            if not required.issubset(raw):
                raise ValueError("incomplete NPC state")
            result[npc_id] = raw | {"position": position}
        return result

    @staticmethod
    def _eggs(data):
        if not isinstance(data, list) or len(data) > 6:
            raise ValueError("invalid Nursery state")
        eggs = []
        for raw in data:
            species = DATABASE.get_species(raw["species"])
            required, walked = raw["steps_required"], raw["steps_walked"]
            if not isinstance(required, int) or not isinstance(walked, int) or required <= 0 or walked < 0:
                raise ValueError("invalid Egg progress")
            move = raw.get("inherited_move")
            if move is not None:
                DATABASE.get_move(move)
            eggs.append(Egg(species.key, required, walked, move))
        return eggs

    @staticmethod
    def _apply(game, state):
        trainer = state["trainer"]
        for name in ("name", "money", "badges", "pokemon_seen", "pokemon_caught", "steps_taken", "play_time_seconds"):
            setattr(game.player.stats, name, trainer[name])
        game.player_name = game.player.stats.name
        game.world.current_area_id = state["area"].area_id
        game.game_map = state["area"].game_map
        game.player.teleport(*state["position"])
        game.player.direction = state["direction"]
        game.party = state["party"]
        game.inventory = state["inventory"]
        game.quests.progress = state["quests"]
        game.story.active_chapter = state["story"]["active_chapter"]
        game.story.badges = set(state["story"]["badges"])
        game.story.flags = set(state["story"]["flags"])
        game.badge_names = game.story.badges
        for npc_id, raw in state["npcs"].items():
            npc = game.npcs.npcs[npc_id]
            npc.tile_x, npc.tile_y = raw["position"]
            for name in ("direction", "interacted", "defeated", "reward_claimed", "patrol_index", "active_schedule_index"):
                setattr(npc, name, raw[name])
        game.nursery.eggs = state["eggs"]
        game.world_simulation = state["simulation"]
        game.refresh_world_context()
        game.settings = state["settings"]
        game.camera = type(game.camera)(game.game_map.pixel_width, game.game_map.pixel_height)
        game.camera.update(*game.player.center, snap=True)

    @staticmethod
    def _snapshot(game):
        return {
            "schema_version": SAVE_VERSION,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "trainer": asdict(game.player.stats),
            "location": {"area": game.world.current_area_id, "position": [game.player.tile_x, game.player.tile_y], "direction": game.player.direction},
            "party": {"active_index": game.party.active_index, "members": [pokemon.to_dict() for pokemon in game.party.party]},
            "storage": {"boxes": [[pokemon.to_dict() for pokemon in box.pokemon] for box in game.party.storage.boxes]},
            "inventory": game.inventory.to_dict(), "quests": game.quests.to_dict(), "story": game.story.to_dict(),
            "npcs": {npc_id: {"position": list(npc.position), "direction": npc.direction, "interacted": npc.interacted, "defeated": npc.defeated, "reward_claimed": npc.reward_claimed, "patrol_index": npc.patrol_index, "active_schedule_index": npc.active_schedule_index} for npc_id, npc in game.npcs.npcs.items()},
            "nursery": game.nursery.to_dict(),
            "encounter_context": asdict(game.encounter_context),
            "world_simulation": game.world_simulation.to_dict(),
            "settings": asdict(game.settings),
        }
