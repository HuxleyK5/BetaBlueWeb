"""Data-driven NPC definitions, runtime state, movement, and schedules."""

from dataclasses import dataclass, field
import json
from pathlib import Path
import random

import pygame

from .config import PROJECT_ROOT, TILE_SIZE
from .items import ITEM_DATABASE
from .pokemon_data import DATABASE, create_pokemon


NPC_ROLES = {"resident", "quest", "trainer", "rival", "gym_leader", "shopkeeper"}
TRAINER_ROLES = {"trainer", "rival", "gym_leader"}
ROLE_COLORS = {
    "resident": (87, 132, 194), "quest": (153, 94, 190), "trainer": (203, 116, 55),
    "rival": (218, 74, 78), "gym_leader": (234, 185, 49), "shopkeeper": (63, 166, 137),
}


class NPCDataError(ValueError):
    """Raised when NPC data references invalid world or game content."""


@dataclass
class NPC:
    npc_id: str
    name: str
    area_id: str
    role: str
    tile_x: int
    tile_y: int
    direction: str
    dialogue: tuple[str, ...]
    post_dialogue: tuple[str, ...]
    movement: str
    patrol: tuple[tuple[int, int], ...]
    schedule: tuple[dict, ...]
    party_specs: tuple[dict, ...]
    reward: dict
    shop: tuple[dict, ...]
    ai: str = "balanced"
    interacted: bool = False
    defeated: bool = False
    reward_claimed: bool = False
    move_timer: float = 0.0
    patrol_index: int = 0
    active_schedule_index: int = -1

    @property
    def position(self):
        return self.tile_x, self.tile_y

    @property
    def is_trainer(self):
        return self.role in TRAINER_ROLES

    def can_battle(self):
        return self.is_trainer and not self.defeated and bool(self.party_specs)

    def dialogue_for_state(self):
        return self.post_dialogue if (self.interacted or self.defeated or self.reward_claimed) and self.post_dialogue else self.dialogue

    def create_party(self):
        return [create_pokemon(entry["species"], entry["level"]) for entry in self.party_specs]

    def draw(self, surface, offset_x, offset_y, small_font):
        x = round(offset_x + self.tile_x * TILE_SIZE)
        y = round(offset_y + self.tile_y * TILE_SIZE)
        pygame.draw.ellipse(surface, (35, 65, 65), (x + 7, y + 31, 26, 8))
        pygame.draw.circle(surface, ROLE_COLORS[self.role], (x + 20, y + 18), 14)
        pygame.draw.rect(surface, ROLE_COLORS[self.role], (x + 9, y + 18, 22, 18), border_radius=6)
        pygame.draw.circle(surface, (247, 214, 181), (x + 20, y + 12), 8)
        if self.can_battle():
            marker = small_font.render("!", True, (255, 238, 92))
            surface.blit(marker, marker.get_rect(center=(x + 20, y - 5)))


class NPCManager:
    def __init__(self, world, data_path=None, rng=None):
        self.world = world
        self.data_path = Path(data_path or PROJECT_ROOT / "characters" / "npcs.json")
        self.rng = rng or random.Random()
        self.npcs = self._load()

    def in_area(self, area_id):
        return [npc for npc in self.npcs.values() if npc.area_id == area_id]

    def at(self, area_id, tile_x, tile_y):
        return next((npc for npc in self.in_area(area_id) if npc.position == (tile_x, tile_y)), None)

    def is_occupied(self, area_id, tile_x, tile_y):
        return self.at(area_id, tile_x, tile_y) is not None

    def update(self, dt, area_id, world_hour, player_position):
        occupied = {npc.position for npc in self.in_area(area_id)} | {player_position}
        for npc in self.in_area(area_id):
            self._apply_schedule(npc, world_hour, occupied)
            if npc.movement == "stationary":
                continue
            npc.move_timer += dt
            if npc.move_timer < 1.5:
                continue
            npc.move_timer = 0.0
            destination = self._next_destination(npc)
            if destination == npc.position or destination in occupied:
                continue
            area = self.world.areas[area_id]
            if area.game_map.is_solid(*destination) or area.transition_at(*destination):
                continue
            occupied.remove(npc.position)
            old_x, old_y = npc.position
            npc.tile_x, npc.tile_y = destination
            occupied.add(destination)
            npc.direction = _direction_from_delta(destination[0] - old_x, destination[1] - old_y)

    def _next_destination(self, npc):
        if npc.movement == "patrol" and npc.patrol:
            target = npc.patrol[npc.patrol_index]
            if npc.position == target:
                npc.patrol_index = (npc.patrol_index + 1) % len(npc.patrol)
                target = npc.patrol[npc.patrol_index]
            dx = 0 if target[0] == npc.tile_x else 1 if target[0] > npc.tile_x else -1
            dy = 0 if target[1] == npc.tile_y or dx else 1 if target[1] > npc.tile_y else -1
            return npc.tile_x + dx, npc.tile_y + dy
        dx, dy = self.rng.choice(((0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)))
        return npc.tile_x + dx, npc.tile_y + dy

    @staticmethod
    def _apply_schedule(npc, hour, occupied):
        for index, entry in enumerate(npc.schedule):
            if entry["start"] <= hour < entry["end"]:
                if npc.active_schedule_index == index:
                    return
                destination = tuple(entry["position"])
                if destination != npc.position and destination not in occupied:
                    occupied.discard(npc.position)
                    npc.tile_x, npc.tile_y = destination
                    occupied.add(destination)
                npc.active_schedule_index = index
                return

    def _load(self):
        try:
            records = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise NPCDataError(f"Could not load NPC data: {error}") from error
        if not isinstance(records, list):
            raise NPCDataError("NPC data must contain a JSON list")
        npcs = {}
        occupied = set()
        for raw in records:
            try:
                npc = NPC(
                    raw["id"], raw["name"], raw["area"], raw["role"], *raw["position"],
                    raw.get("direction", "down"), tuple(raw["dialogue"]), tuple(raw.get("post_dialogue", [])),
                    raw.get("movement", "stationary"), tuple(tuple(point) for point in raw.get("patrol", [])),
                    tuple(raw.get("schedule", [])), tuple(raw.get("party", [])), raw.get("reward", {}),
                    tuple(raw.get("shop", [])), raw.get("ai", "balanced"),
                )
            except (KeyError, TypeError) as error:
                raise NPCDataError(f"Invalid NPC record: {raw.get('id', raw)}") from error
            if npc.npc_id in npcs or (npc.area_id, npc.position) in occupied:
                raise NPCDataError(f"Duplicate NPC id or position for '{npc.npc_id}'")
            self._validate(npc)
            npcs[npc.npc_id] = npc
            occupied.add((npc.area_id, npc.position))
        return npcs

    def _validate(self, npc):
        if npc.role not in NPC_ROLES or npc.movement not in {"stationary", "wander", "patrol"}:
            raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid role or movement mode")
        if not npc.dialogue or npc.ai not in {"random", "balanced", "smart", "expert"}:
            raise NPCDataError(f"NPC '{npc.npc_id}' has invalid dialogue or AI")
        area = self.world.areas.get(npc.area_id)
        if area is None or area.game_map.is_solid(*npc.position) or area.transition_at(*npc.position):
            raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid world position")
        for point in npc.patrol:
            if area.game_map.is_solid(*point) or area.transition_at(*point):
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid patrol point")
        for entry in npc.schedule:
            position = entry.get("position", ())
            if not isinstance(entry.get("start"), int) or not isinstance(entry.get("end"), int) or not 0 <= entry["start"] < entry["end"] <= 24:
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid schedule time")
            if len(position) != 2 or area.game_map.is_solid(*position) or area.transition_at(*position):
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid schedule position")
        for member in npc.party_specs:
            if member.get("species") not in DATABASE.species or not 1 <= member.get("level", 0) <= 100:
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid party member")
        for offer in npc.shop:
            if offer.get("item") not in ITEM_DATABASE or not isinstance(offer.get("price"), int) or offer["price"] <= 0:
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid shop offer")
        for item_id, count in npc.reward.get("items", {}).items():
            if item_id not in ITEM_DATABASE or not isinstance(count, int) or count <= 0:
                raise NPCDataError(f"NPC '{npc.npc_id}' has an invalid item reward")


def _direction_from_delta(dx, dy):
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"
