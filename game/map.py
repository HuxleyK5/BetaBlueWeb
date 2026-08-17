"""Tile definitions, map validation, collision, and visible-tile rendering."""

from dataclasses import dataclass

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE


@dataclass(frozen=True)
class TileDefinition:
    name: str
    color: tuple[int, int, int]
    solid: bool = False


TILES = {
    ".": TileDefinition("grass", (78, 188, 98)),
    "P": TileDefinition("path", (218, 190, 135)),
    "W": TileDefinition("water", (66, 135, 245), True),
    "T": TileDefinition("tree", (45, 139, 67), True),
    "B": TileDefinition("building", (184, 172, 145), True),
    "M": TileDefinition("mountain", (116, 108, 102), True),
    "G": TileDefinition("tall_grass", (45, 158, 77)),
    "F": TileDefinition("flower", (238, 116, 157)),
    "C": TileDefinition("cave", (82, 76, 76)),
}

# Compatibility names used by systems scheduled for later modular migration.
TILE_GRASS = "."
TILE_PATH = "P"
TILE_WATER = "W"
TILE_TREE = "T"
TILE_BUILDING = "B"
TILE_MOUNTAIN = "M"
TILE_TALL_GRASS = "G"
TILE_FLOWER = "F"
TILE_CAVE = "C"


class MapDataError(ValueError):
    """Raised when an area data file cannot produce a safe playable map."""


class GameMap:
    def __init__(self, tile_rows):
        if not tile_rows or not isinstance(tile_rows, list):
            raise MapDataError("Map must contain at least one tile row")
        self.tile_rows = tuple(tile_rows)
        self.width = len(self.tile_rows[0])
        self.height = len(self.tile_rows)
        if not self.width or any(len(row) != self.width for row in self.tile_rows):
            raise MapDataError("All map rows must have the same non-zero width")
        unknown = sorted({symbol for row in self.tile_rows for symbol in row if symbol not in TILES})
        if unknown:
            raise MapDataError(f"Unknown tile symbols: {', '.join(unknown)}")

    @property
    def pixel_width(self):
        return self.width * TILE_SIZE

    @property
    def pixel_height(self):
        return self.height * TILE_SIZE

    def contains(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def tile_at(self, x, y):
        return TILES[self.tile_rows[y][x]] if self.contains(x, y) else None

    def symbol_at(self, x, y):
        return self.tile_rows[y][x] if self.contains(x, y) else None

    def is_solid(self, x, y):
        tile = self.tile_at(x, y)
        return tile is None or tile.solid

    def draw(self, surface, offset_x=0, offset_y=0):
        """Draw only tiles intersecting the camera viewport."""
        start_x = max(0, int(-offset_x // TILE_SIZE))
        start_y = max(0, int(-offset_y // TILE_SIZE))
        end_x = min(self.width, start_x + SCREEN_WIDTH // TILE_SIZE + 2)
        end_y = min(self.height, start_y + SCREEN_HEIGHT // TILE_SIZE + 2)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = TILES[self.tile_rows[y][x]]
                rect = pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, tile.color, rect)
                self._draw_detail(surface, rect, tile.name, x, y)

    @staticmethod
    def _draw_detail(surface, rect, tile_name, x, y):
        if tile_name == "water":
            pygame.draw.line(surface, (126, 202, 250), (rect.x + 7, rect.y + 13), (rect.right - 7, rect.y + 13), 2)
        elif tile_name == "tree":
            pygame.draw.circle(surface, (85, 185, 80), rect.center, 14)
            pygame.draw.rect(surface, (100, 70, 45), (rect.centerx - 3, rect.bottom - 10, 6, 9))
        elif tile_name == "building":
            pygame.draw.rect(surface, (211, 82, 75), (rect.x + 2, rect.y + 3, rect.width - 4, 12))
        elif tile_name == "mountain":
            pygame.draw.polygon(surface, (158, 148, 134), [(rect.x + 3, rect.bottom - 3), (rect.centerx, rect.y + 4), (rect.right - 3, rect.bottom - 3)])
        elif tile_name == "tall_grass":
            for blade_x in (8, 18, 29):
                pygame.draw.line(surface, (25, 117, 61), (rect.x + blade_x, rect.bottom - 5), (rect.x + blade_x - 4, rect.y + 12), 2)
        elif tile_name == "flower":
            color = (255, 225, 82) if (x + y) % 2 else (255, 239, 245)
            pygame.draw.circle(surface, color, rect.center, 5)
        elif tile_name == "cave":
            pygame.draw.circle(surface, (108, 99, 96), (rect.x + 9, rect.y + 11), 3)
            pygame.draw.circle(surface, (58, 53, 54), (rect.x + 28, rect.y + 27), 4)
