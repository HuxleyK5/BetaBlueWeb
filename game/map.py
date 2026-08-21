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
        self._render_cache = None

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
        """Blit the static map layer; tile art is generated only once per area."""
        if self._render_cache is None:
            self._render_cache = pygame.Surface((self.pixel_width, self.pixel_height)).convert()
            for y in range(self.height):
                for x in range(self.width):
                    tile = TILES[self.tile_rows[y][x]]
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self._render_cache, tile.color, rect)
                    self._draw_detail(self._render_cache, rect, tile.name, x, y)
        surface.blit(self._render_cache, (round(offset_x), round(offset_y)))
        self._draw_animated_details(surface, round(offset_x), round(offset_y))

    @staticmethod
    def _draw_detail(surface, rect, tile_name, x, y):
        if tile_name == "grass":
            shade = (92, 203, 111) if (x + y) % 2 else (72, 181, 91)
            for dot_x, dot_y in ((8, 9), (27, 18), (15, 31)):
                if (x * 7 + y * 5 + dot_x) % 3:
                    pygame.draw.rect(surface, shade, (rect.x + dot_x, rect.y + dot_y, 2, 2))
        elif tile_name == "path":
            pygame.draw.rect(surface, (239, 218, 165), rect.inflate(-4, -4), 1, border_radius=4)
            if (x + y) % 2 == 0:
                pygame.draw.circle(surface, (185, 154, 102), (rect.x + 10, rect.y + 27), 2)
                pygame.draw.circle(surface, (185, 154, 102), (rect.x + 29, rect.y + 12), 1)
        elif tile_name == "water":
            pygame.draw.rect(surface, (47, 112, 206), rect, 1)
        elif tile_name == "tree":
            pygame.draw.rect(surface, (100, 70, 45), (rect.centerx - 4, rect.bottom - 13, 8, 12))
            pygame.draw.circle(surface, (29, 113, 56), (rect.centerx, rect.y + 20), 17)
            pygame.draw.circle(surface, (72, 178, 73), (rect.centerx - 7, rect.y + 15), 12)
            pygame.draw.circle(surface, (102, 204, 82), (rect.centerx + 7, rect.y + 13), 10)
            pygame.draw.circle(surface, (151, 224, 100), (rect.centerx + 4, rect.y + 9), 4)
        elif tile_name == "building":
            pygame.draw.rect(surface, (39, 55, 74), rect.inflate(-2, -6), 2, border_radius=5)
            pygame.draw.rect(surface, (211, 82, 75), (rect.x + 2, rect.y + 3, rect.width - 4, 13), border_radius=5)
            pygame.draw.line(surface, (247, 157, 105), (rect.x + 6, rect.y + 8), (rect.right - 6, rect.y + 8), 2)
            pygame.draw.rect(surface, (111, 78, 55), (rect.centerx - 5, rect.y + 22, 10, 15), border_radius=2)
        elif tile_name == "mountain":
            points = [(rect.x + 2, rect.bottom - 2), (rect.centerx, rect.y + 3), (rect.right - 2, rect.bottom - 2)]
            pygame.draw.polygon(surface, (76, 74, 78), points)
            pygame.draw.polygon(surface, (161, 153, 143), [(rect.x + 8, rect.bottom - 3), (rect.centerx, rect.y + 8), (rect.centerx + 4, rect.bottom - 3)])
            pygame.draw.polygon(surface, (226, 224, 211), [(rect.centerx - 6, rect.y + 12), (rect.centerx, rect.y + 3), (rect.centerx + 7, rect.y + 13)])
        elif tile_name == "tall_grass":
            pygame.draw.rect(surface, (38, 136, 69), rect, 1)
        elif tile_name == "flower":
            color = (255, 225, 82) if (x + y) % 2 else (255, 239, 245)
            pygame.draw.circle(surface, color, rect.center, 5)
        elif tile_name == "cave":
            pygame.draw.circle(surface, (108, 99, 96), (rect.x + 9, rect.y + 11), 3)
            pygame.draw.circle(surface, (58, 53, 54), (rect.x + 28, rect.y + 27), 4)

    def _draw_animated_details(self, surface, offset_x, offset_y):
        """Animate only water and tall grass over the cached static layer."""
        phase = pygame.time.get_ticks() // 180
        for y, row in enumerate(self.tile_rows):
            screen_y = offset_y + y * TILE_SIZE
            if screen_y > SCREEN_HEIGHT or screen_y + TILE_SIZE < 0:
                continue
            for x, symbol in enumerate(row):
                if symbol not in {"W", "G"}:
                    continue
                screen_x = offset_x + x * TILE_SIZE
                if screen_x > SCREEN_WIDTH or screen_x + TILE_SIZE < 0:
                    continue
                if symbol == "W":
                    shift = (phase + x + y) % 7
                    pygame.draw.line(surface, (138, 213, 252), (screen_x + 3 + shift, screen_y + 10), (screen_x + 16 + shift, screen_y + 10), 2)
                    pygame.draw.line(surface, (111, 193, 245), (screen_x + 17 - shift // 2, screen_y + 27), (screen_x + 34 - shift // 2, screen_y + 27), 2)
                else:
                    sway = ((phase + x + y) % 5) - 2
                    for blade_x in (6, 13, 21, 29, 36):
                        pygame.draw.line(surface, (22, 112, 56), (screen_x + blade_x, screen_y + 35), (screen_x + blade_x + sway, screen_y + 13), 3)
