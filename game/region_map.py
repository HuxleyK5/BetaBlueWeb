"""Data-driven regional overview loading and presentation."""

from dataclasses import dataclass
import json
from pathlib import Path

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH


class RegionMapDataError(ValueError):
    """Raised when region overview content cannot be used safely."""


@dataclass(frozen=True)
class RegionLocation:
    area_id: str
    name: str
    position: tuple[int, int]
    marker: str
    label_offset: tuple[int, int]
    requires_flag: str | None = None


class RegionMap:
    """Validate overview data once and draw it independently from world logic."""

    MARKER_COLORS = {
        "town": (42, 92, 218), "city": (222, 52, 48), "wild": (48, 145, 73),
        "route": (230, 170, 35), "secret": (139, 75, 190),
    }

    def __init__(self, data_path, known_areas):
        self.data_path = Path(data_path)
        try:
            data = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise RegionMapDataError(f"Invalid region map {self.data_path.name}: {error}") from error
        try:
            self.region_id, self.name = data["id"], data["name"]
            self.background = data["background"]
            raw_locations, raw_connections = data["locations"], data["connections"]
        except (KeyError, TypeError) as error:
            raise RegionMapDataError(f"Region map is missing required data: {error}") from error
        if not all(isinstance(value, str) and value for value in (self.region_id, self.name, self.background)):
            raise RegionMapDataError("Region id, name, and background must be non-empty strings")

        self.locations = {}
        for item in raw_locations:
            try:
                area_id = item["area"]
                position = tuple(item["position"])
                offset = tuple(item.get("label_offset", (14, -12)))
                marker, required = item.get("marker", "route"), item.get("requires_flag")
            except (KeyError, TypeError) as error:
                raise RegionMapDataError(f"Invalid location record: {error}") from error
            if area_id not in known_areas:
                raise RegionMapDataError(f"Region location targets unknown area '{area_id}'")
            if area_id in self.locations:
                raise RegionMapDataError(f"Duplicate region location '{area_id}'")
            if marker not in self.MARKER_COLORS:
                raise RegionMapDataError(f"Unknown marker style '{marker}'")
            if not self._valid_pair(position, positive=True) or not self._valid_pair(offset):
                raise RegionMapDataError(f"Invalid coordinates for region location '{area_id}'")
            if required is not None and (not isinstance(required, str) or not required):
                raise RegionMapDataError(f"Invalid required flag for '{area_id}'")
            self.locations[area_id] = RegionLocation(
                area_id, known_areas[area_id].name, position, marker, offset, required
            )

        self.connections = []
        for connection in raw_connections:
            if not isinstance(connection, list) or len(connection) != 2:
                raise RegionMapDataError("Every region connection must contain two area ids")
            start, end = connection
            if start not in self.locations or end not in self.locations:
                raise RegionMapDataError(f"Region connection references an unknown location: {connection}")
            self.connections.append((start, end))

    @staticmethod
    def _valid_pair(value, positive=False):
        return len(value) == 2 and all(
            isinstance(number, int) and not isinstance(number, bool) and (not positive or number >= 0)
            for number in value
        )

    def visible_locations(self, story_flags):
        return {
            area_id: location for area_id, location in self.locations.items()
            if location.requires_flag is None or location.requires_flag in story_flags
        }

    def draw(self, surface, assets, current_area_id, story_flags, fonts):
        """Draw the background, route network, markers, and current position."""
        title_font, body_font, small_font = fonts
        surface.blit(assets.image(self.background, size=(SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        visible = self.visible_locations(story_flags)

        for start_id, end_id in self.connections:
            if start_id in visible and end_id in visible:
                start, end = visible[start_id].position, visible[end_id].position
                pygame.draw.line(surface, (90, 94, 98), start, end, 13)
                pygame.draw.line(surface, (248, 248, 242), start, end, 7)

        for location in visible.values():
            active = location.area_id == current_area_id
            radius = 12 if active else 9
            pygame.draw.circle(surface, (32, 37, 47), location.position, radius + 4)
            pygame.draw.circle(
                surface, (255, 224, 90) if active else self.MARKER_COLORS[location.marker],
                location.position, radius,
            )
            if active:
                pygame.draw.circle(surface, (255, 255, 255), location.position, radius + 8, 3)
            label = body_font.render(location.name, True, (21, 30, 39))
            label_pos = (location.position[0] + location.label_offset[0], location.position[1] + location.label_offset[1])
            plate = label.get_rect(topleft=label_pos).inflate(10, 6)
            plate_surface = pygame.Surface(plate.size, pygame.SRCALPHA)
            plate_surface.fill((246, 250, 242, 215))
            surface.blit(plate_surface, plate.topleft)
            surface.blit(label, label_pos)

        header = pygame.Surface((SCREEN_WIDTH, 58), pygame.SRCALPHA)
        header.fill((16, 35, 64, 220))
        surface.blit(header, (0, 0))
        surface.blit(title_font.render(self.name, True, (255, 235, 130)), (22, 7))
        current_name = self.locations[current_area_id].name if current_area_id in self.locations else "Unknown"
        subtitle = small_font.render(f"Current location: {current_name}", True, (235, 243, 255))
        surface.blit(subtitle, (SCREEN_WIDTH - subtitle.get_width() - 20, 19))
        footer = pygame.Surface((SCREEN_WIDTH, 35), pygame.SRCALPHA)
        footer.fill((16, 35, 64, 220))
        surface.blit(footer, (0, SCREEN_HEIGHT - 35))
        hint = small_font.render("R or ESC: return to exploration", True, (240, 246, 255))
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))
