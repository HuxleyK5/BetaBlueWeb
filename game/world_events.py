"""Validated timed events and story-gated hidden map connections."""

from dataclasses import dataclass
import json
from pathlib import Path

from .encounters import EncounterContext
from .world import Transition
from .weather import SEASONS, WEATHER


class WorldEventDataError(ValueError):
    pass


@dataclass(frozen=True)
class WorldEvent:
    event_id: str
    name: str
    areas: tuple[str, ...]
    conditions: dict
    weather_override: str | None = None


@dataclass(frozen=True)
class HiddenTransition:
    transition_id: str
    area: str
    position: tuple[int, int]
    transition: Transition
    conditions: dict


class WorldEventManager:
    def __init__(self, data_path, world):
        self.data_path, self.world = Path(data_path), world
        self.events, self.hidden_transitions = self._load()

    def context_for(self, area_id, simulation, story_flags):
        base = EncounterContext(simulation.weather, simulation.season, simulation.time_of_day)
        for event in self.active_events(area_id, simulation, story_flags):
            if event.weather_override:
                return EncounterContext(event.weather_override, simulation.season, simulation.time_of_day)
        return base

    def active_events(self, area_id, simulation, story_flags):
        return [event for event in self.events if area_id in event.areas and self._matches(event.conditions, simulation, story_flags)]

    def transition_at(self, area_id, tile_x, tile_y, simulation, story_flags):
        for hidden in self.hidden_transitions:
            if hidden.area == area_id and hidden.position == (tile_x, tile_y) and self._matches(hidden.conditions, simulation, story_flags):
                return hidden.transition
        return None

    def active_hidden_transitions(self, area_id, simulation, story_flags):
        return [hidden for hidden in self.hidden_transitions if hidden.area == area_id and self._matches(hidden.conditions, simulation, story_flags)]

    @staticmethod
    def _matches(conditions, simulation, story_flags):
        for key, required in conditions.items():
            if key == "flags":
                values = required if isinstance(required, list) else [required]
                if not set(values).issubset(story_flags):
                    return False
            else:
                options = required if isinstance(required, list) else [required]
                if getattr(simulation, key, None) not in options:
                    return False
        return True

    def _load(self):
        try:
            raw = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise WorldEventDataError(f"Could not load world events: {error}") from error
        events, hidden, identifiers = [], [], set()
        try:
            for item in raw.get("events", []):
                event = WorldEvent(item["id"], item["name"], tuple(item["areas"]), item.get("conditions", {}), item.get("weather_override"))
                if event.event_id in identifiers or not set(event.areas).issubset(self.world.areas):
                    raise WorldEventDataError(f"Event '{event.event_id}' references an unknown area")
                self._validate_conditions(event.event_id, event.conditions)
                if event.weather_override is not None and event.weather_override not in set(WEATHER) | {"starfall"}:
                    raise WorldEventDataError(f"Event '{event.event_id}' has invalid weather")
                identifiers.add(event.event_id)
                events.append(event)
            for item in raw.get("hidden_transitions", []):
                entry = HiddenTransition(item["id"], item["area"], tuple(item["at"]), Transition(item["target"], tuple(item["destination"])), item.get("conditions", {}))
                if entry.transition_id in identifiers or entry.area not in self.world.areas or entry.transition.target_area not in self.world.areas:
                    raise WorldEventDataError(f"Hidden transition '{entry.transition_id}' references an unknown area")
                self._validate_conditions(entry.transition_id, entry.conditions)
                source, target = self.world.areas[entry.area], self.world.areas[entry.transition.target_area]
                if source.game_map.is_solid(*entry.position) or target.game_map.is_solid(*entry.transition.destination):
                    raise WorldEventDataError(f"Hidden transition '{entry.transition_id}' has a blocked coordinate")
                identifiers.add(entry.transition_id)
                hidden.append(entry)
        except (KeyError, TypeError) as error:
            raise WorldEventDataError(f"Invalid world event record: {error}") from error
        return tuple(events), tuple(hidden)

    @staticmethod
    def _validate_conditions(identifier, conditions):
        if not isinstance(conditions, dict) or not set(conditions).issubset({"flags", "season", "time_of_day", "weather"}):
            raise WorldEventDataError(f"'{identifier}' has invalid event conditions")
        valid = {
            "season": set(SEASONS), "time_of_day": {"dawn", "day", "dusk", "night"},
            "weather": set(WEATHER) | {"starfall"},
        }
        for key, required in conditions.items():
            values = required if isinstance(required, list) else [required]
            if not values or (key == "flags" and not all(isinstance(value, str) and value for value in values)):
                raise WorldEventDataError(f"'{identifier}' has invalid '{key}' conditions")
            if key in valid and not set(values).issubset(valid[key]):
                raise WorldEventDataError(f"'{identifier}' has invalid '{key}' conditions")
