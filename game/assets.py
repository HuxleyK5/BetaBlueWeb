"""Centralized, cached asset loading with development-safe fallbacks."""

from pathlib import Path
from typing import Optional

import pygame

from .config import ASSET_FOLDERS, PROJECT_ROOT, USER_DATA_ROOT


class AssetManager:
    """Resolve assets from the project root and avoid loading files repeatedly."""

    def __init__(self, root: Path = PROJECT_ROOT):
        self.root = Path(root)
        self._images: dict[tuple[str, Optional[tuple[int, int]]], pygame.Surface] = {}
        self._fonts: dict[tuple[Optional[str], int, bool], pygame.font.Font] = {}

    def image(self, relative_path, size=None, fallback_color=(255, 0, 255)):
        key = (str(relative_path), size)
        if key not in self._images:
            path = self.root / relative_path
            try:
                image = pygame.image.load(path).convert_alpha()
            except (FileNotFoundError, pygame.error):
                image = self._missing_image(size or (32, 32), fallback_color)
            if size is not None and image.get_size() != size:
                image = pygame.transform.scale(image, size)
            self._images[key] = image
        return self._images[key]

    def font(self, size, bold=False, relative_path=None):
        key = (str(relative_path) if relative_path else None, size, bold)
        if key not in self._fonts:
            path = self.root / relative_path if relative_path else None
            font = pygame.font.Font(path, size)
            font.set_bold(bold)
            self._fonts[key] = font
        return self._fonts[key]

    def preload_images(self, paths, size=None):
        """Warm frequently used images once, before their first animated screen."""
        for path in paths:
            self.image(path, size=size)

    def cache_stats(self):
        return {"images": len(self._images), "fonts": len(self._fonts)}

    @staticmethod
    def _missing_image(size, color):
        image = pygame.Surface(size, pygame.SRCALPHA)
        image.fill(color)
        pygame.draw.line(image, (0, 0, 0), (0, 0), (size[0] - 1, size[1] - 1), 2)
        pygame.draw.line(image, (0, 0, 0), (size[0] - 1, 0), (0, size[1] - 1), 2)
        return image


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


def ensure_asset_folders(root_path, user_data_root=USER_DATA_ROOT):
    root = Path(root_path)
    for folder in ASSET_FOLDERS:
        target = Path(user_data_root) / folder if folder == "saves" else root / folder
        target.mkdir(parents=True, exist_ok=True)
