"""Project paths, configuration defaults, and settings loading."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
USER_DATA_ROOT = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local" / "share")) / "PokemonBetaBlue" if getattr(sys, "frozen", False) else PROJECT_ROOT
SETTINGS_PATH = USER_DATA_ROOT / "settings.json" if getattr(sys, "frozen", False) else Path(__file__).with_name("settings.json")
GAME_VERSION = "0.15.0-beta"

# Screen and tile configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
MAP_WIDTH = 20
MAP_HEIGHT = 15
FPS = 60

# Player defaults
PLAYER_START_X = 10
PLAYER_START_Y = 7
PLAYER_SPEED = 200  # pixels per second; independent of frame rate
PLAYER_ANIMATION_FPS = 8
CAMERA_FOLLOW_SPEED = 10.0

# Game state identifiers
STATE_TITLE = "title"
STATE_NAME_ENTRY = "name_entry"
STATE_STARTER_SELECT = "starter_select"
STATE_TOWN = "town"
STATE_BUILDING = "building"
STATE_ROUTE_EXPLORE = "route_explore"
STATE_BATTLE = "battle"
STATE_WILD_ENCOUNTER = "wild_encounter"
STATE_DIALOGUE = "dialogue"
STATE_SHOP = "shop"
STATE_QUEST_LOG = "quest_log"
STATE_INVENTORY = "inventory"
STATE_NURSERY = "nursery"
STATE_MULTIPLAYER = "multiplayer"
STATE_REGION_MAP = "region_map"
STATE_MENU = "menu"

# Asset folders
ASSET_FOLDERS = [
    "assets",
    "sprites",
    "maps",
    "characters",
    "pokemon",
    "battles",
    "items",
    "UI",
    "sounds",
    "saves",
    "scripts",
    "quests",
]

# Input options
MAX_PLAYER_NAME_LENGTH = 12


@dataclass(frozen=True)
class Settings:
    """Validated runtime options loaded from ``settings.json``."""

    window_width: int = SCREEN_WIDTH
    window_height: int = SCREEN_HEIGHT
    fullscreen: bool = False
    vsync: bool = True
    target_fps: int = FPS
    master_volume: float = 0.7
    sfx_volume: float = 0.8


def _positive_int(value: Any, fallback: int) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else fallback


def _volume(value, fallback):
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1 else fallback


def load_settings(path: Path = SETTINGS_PATH) -> Settings:
    """Load user-editable settings, falling back safely when data is invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return Settings()

    if not isinstance(data, dict):
        return Settings()
    return Settings(
        window_width=_positive_int(data.get("window_width"), SCREEN_WIDTH),
        window_height=_positive_int(data.get("window_height"), SCREEN_HEIGHT),
        fullscreen=data.get("fullscreen") if isinstance(data.get("fullscreen"), bool) else False,
        vsync=data.get("vsync") if isinstance(data.get("vsync"), bool) else True,
        target_fps=_positive_int(data.get("target_fps"), FPS),
        master_volume=_volume(data.get("master_volume"), 0.7),
        sfx_volume=_volume(data.get("sfx_volume"), 0.8),
    )


def save_settings(settings, path: Path = SETTINGS_PATH):
    """Atomically persist validated application preferences."""
    temporary = path.with_suffix(".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(json.dumps({
        "window_width": settings.window_width, "window_height": settings.window_height,
        "fullscreen": settings.fullscreen, "vsync": settings.vsync,
        "target_fps": settings.target_fps,
        "master_volume": settings.master_volume, "sfx_volume": settings.sfx_volume,
    }, indent=2), encoding="utf-8")
    temporary.replace(path)
