"""Game configuration constants and defaults."""

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
PLAYER_SPEED = 4  # pixels per frame for smooth movement

# Game state identifiers
STATE_TITLE = "title"
STATE_NAME_ENTRY = "name_entry"
STATE_TOWN = "town"
STATE_BUILDING = "building"
STATE_ROUTE_EXPLORE = "route_explore"
STATE_BATTLE = "battle"
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
