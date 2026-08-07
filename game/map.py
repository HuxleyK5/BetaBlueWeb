"""Basic tile-based map system for Pokemon Beta Blue."""

import pygame

from .config import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT


TILE_GRASS = 0
TILE_PATH = 1
TILE_WATER = 2
TILE_TREE = 3
TILE_BUILDING = 4

SOLID_TILES = {TILE_WATER, TILE_TREE, TILE_BUILDING}

SAMPLE_TOWN_MAP = [
    [TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE, TILE_TREE],
] + [
    [TILE_GRASS] * MAP_WIDTH for _ in range(MAP_HEIGHT - 10)
] + [
    [TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE],
    [TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE],
]


class GameMap:
    def __init__(self, tile_map=None):
        self.tile_map = tile_map if tile_map is not None else SAMPLE_TOWN_MAP
        self.width = len(self.tile_map[0])
        self.height = len(self.tile_map)

    def is_solid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.tile_map[y][x] in SOLID_TILES

    def draw(self, surface, offset_x=0, offset_y=0):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                tile_rect = pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == TILE_GRASS:
                    pygame.draw.rect(surface, (78, 188, 98), tile_rect)
                elif tile == TILE_PATH:
                    pygame.draw.rect(surface, (210, 180, 140), tile_rect)
                elif tile == TILE_WATER:
                    pygame.draw.rect(surface, (66, 135, 245), tile_rect)
                elif tile == TILE_TREE:
                    pygame.draw.rect(surface, (55, 147, 72), tile_rect)
                elif tile == TILE_BUILDING:
                    pygame.draw.rect(surface, (180, 170, 140), tile_rect)
                pygame.draw.rect(surface, (0, 0, 0), tile_rect, 1)
