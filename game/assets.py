"""Asset management system for Pokemon Beta Blue."""

import pygame
from pathlib import Path


def load_image(name, folder, fallback_color=(255, 0, 255)):
    path = Path(folder) / name
    if path.exists():
        image = pygame.image.load(path).convert_alpha()
        return image

    image = pygame.Surface((32, 32), pygame.SRCALPHA)
    image.fill(fallback_color)
    pygame.draw.line(image, (0, 0, 0), (0, 0), (32, 32), 2)
    pygame.draw.line(image, (0, 0, 0), (32, 0), (0, 32), 2)
    return image


def load_font(size, bold=False):
    return pygame.font.Font(None, size)


def ensure_asset_folders(root_path):
    folders = [
        root_path / "assets",
        root_path / "sprites",
        root_path / "maps",
        root_path / "characters",
        root_path / "pokemon",
        root_path / "battles",
        root_path / "items",
        root_path / "UI",
        root_path / "sounds",
        root_path / "saves",
        root_path / "scripts",
        root_path / "quests",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
