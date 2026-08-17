"""Data-driven connected-area loading and travel management."""

from dataclasses import dataclass
import json
from pathlib import Path

from .config import PROJECT_ROOT
from .map import GameMap, MapDataError


@dataclass(frozen=True)
class Transition:
    target_area: str
    destination: tuple[int, int]


@dataclass(frozen=True)
class Area:
    area_id: str
    name: str
    kind: str
    description: str
    game_map: GameMap
    spawn: tuple[int, int]
    transitions: dict[tuple[int, int], Transition]

    def transition_at(self, tile_x, tile_y):
        return self.transitions.get((tile_x, tile_y))


class WorldDataError(ValueError):
    """Raised when connected-world data is missing or inconsistent."""


class WorldManager:
    def __init__(self, maps_path=None, starting_area="starting_town"):
        self.maps_path = Path(maps_path or PROJECT_ROOT / "maps")
        self.areas = self._load_areas()
        self._validate_connections()
        if starting_area not in self.areas:
            raise WorldDataError(f"Starting area '{starting_area}' does not exist")
        self.current_area_id = starting_area

    @property
    def current_area(self):
        return self.areas[self.current_area_id]

    def transition_at(self, tile_x, tile_y):
        return self.current_area.transition_at(tile_x, tile_y)

    def travel(self, transition):
        self.current_area_id = transition.target_area
        return self.current_area, transition.destination

    def _load_areas(self):
        areas = {}
        for path in sorted(self.maps_path.glob("*.json")):
            area = self._load_area(path)
            if area.area_id in areas:
                raise WorldDataError(f"Duplicate area id '{area.area_id}'")
            areas[area.area_id] = area
        if not areas:
            raise WorldDataError(f"No area files found in {self.maps_path}")
        return areas

    @staticmethod
    def _load_area(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            game_map = GameMap(data["tiles"])
            spawn = tuple(data["spawn"])
            raw_transitions = data.get("transitions", [])
            transitions = {
                tuple(item["at"]): Transition(item["target"], tuple(item["destination"]))
                for item in raw_transitions
            }
            area = Area(data["id"], data["name"], data["kind"], data["description"], game_map, spawn, transitions)
        except (OSError, json.JSONDecodeError, KeyError, TypeError, MapDataError) as error:
            raise WorldDataError(f"Invalid area file {path.name}: {error}") from error
        if len(transitions) != len(raw_transitions):
            raise WorldDataError(f"Area '{area.area_id}' has duplicate transition tiles")
        if not WorldManager._is_open_coordinate(game_map, spawn):
            raise WorldDataError(f"Area '{area.area_id}' has an invalid spawn tile")
        for tile in transitions:
            if not WorldManager._is_open_coordinate(game_map, tile):
                raise WorldDataError(f"Area '{area.area_id}' has an invalid transition tile {tile}")
        return area

    @staticmethod
    def _is_open_coordinate(game_map, coordinate):
        return (
            len(coordinate) == 2
            and all(isinstance(value, int) and not isinstance(value, bool) for value in coordinate)
            and not game_map.is_solid(*coordinate)
        )

    def _validate_connections(self):
        for area in self.areas.values():
            for transition in area.transitions.values():
                target = self.areas.get(transition.target_area)
                if target is None:
                    raise WorldDataError(f"Area '{area.area_id}' targets missing area '{transition.target_area}'")
                if not self._is_open_coordinate(target.game_map, transition.destination):
                    raise WorldDataError(
                        f"Transition from '{area.area_id}' has invalid destination {transition.destination}"
                    )
