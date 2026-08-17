"""Project paths, configuration defaults, and settings loading."""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = Path(__file__).with_name("settings.json")

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


def _positive_int(value: Any, fallback: int) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else fallback


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
    )


def save_settings(settings, path: Path = SETTINGS_PATH):
    """Atomically persist validated application preferences."""
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({
        "window_width": settings.window_width, "window_height": settings.window_height,
        "fullscreen": settings.fullscreen, "vsync": settings.vsync,
        "target_fps": settings.target_fps,
    }, indent=2), encoding="utf-8")
    temporary.replace(path)
