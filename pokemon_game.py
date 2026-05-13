"""
Beta Blue - A Pokemon-style top-down RPG scene.
A 2D handheld-inspired RPG with a title screen, name entry, and town exploration.
"""

import pygame
import sys
import os
import random
import re
from pathlib import Path

# Ask SDL to place the game window in the center of the monitor.
os.environ.setdefault("SDL_VIDEO_CENTERED", "1")

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
MAP_WIDTH = 20
MAP_HEIGHT = 15
MAP_PIXEL_WIDTH = MAP_WIDTH * TILE_SIZE
MAP_PIXEL_HEIGHT = MAP_HEIGHT * TILE_SIZE
MAP_OFFSET_X = (SCREEN_WIDTH - MAP_PIXEL_WIDTH) // 2
MAP_OFFSET_Y = (SCREEN_HEIGHT - MAP_PIXEL_HEIGHT) // 2

# Colors - soft, vibrant handheld palette
GRASS = (102, 204, 116)
GRASS_LIGHT = (133, 222, 139)
GRASS_DARK = (67, 161, 86)
PATH = (232, 204, 142)
PATH_LIGHT = (246, 224, 171)
PATH_DARK = (204, 170, 105)
WATER = (48, 160, 232)
WATER_LIGHT = (112, 211, 255)
WATER_DARK = (31, 119, 202)
BUILDING = (245, 238, 211)
BUILDING_SHADE = (219, 204, 174)
BUILDING_ROOF = (83, 142, 220)
BUILDING_ROOF_DARK = (45, 92, 175)
TREE = (48, 164, 85)
TREE_LIGHT = (91, 207, 112)
TREE_DARK = (33, 128, 70)
TREE_TRUNK = (141, 93, 51)
FLOWER_PINK = (255, 139, 169)
FLOWER_YELLOW = (255, 225, 100)
UI_BG = (42, 84, 143)
UI_PANEL = (247, 251, 255)
OUTLINE = (36, 54, 82)
TEXT_WHITE = (255, 255, 255)
TEXT_GOLD = (255, 228, 96)
TEXT_BLUE = (37, 95, 180)
PLAYER_COLOR = (255, 103, 103)
SAPPHIRE_DEEP = (22, 75, 154)
SAPPHIRE_MID = (48, 139, 219)
SAPPHIRE_LIGHT = (117, 213, 246)
GBA_PANEL_BLUE = (42, 80, 168)
GBA_PANEL_SHADOW = (127, 154, 205)

# Game States
STATE_TITLE = "title"
STATE_NAME_ENTRY = "name_entry"
STATE_TOWN = "town"
STATE_BUILDING = "building"
STATE_ROUTE_EVENT = "route_event"
STATE_BATTLE = "battle"
STATE_NEXT_TOWN = "world_map"
STATE_ROUTE_EXPLORE = "route_explore"
STATE_WILD_ENCOUNTER = "wild_encounter"
STATE_TEST_REGION_PICKER = "test_region_picker"

# Map tiles
TILE_GRASS = 0
TILE_PATH = 1
TILE_BUILDING = 2
TILE_TREE = 3
TILE_WATER = 4
TILE_TALL_GRASS = 5

# Create the town map (20x15)
TOWN_MAP = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 4, 4, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3],
    [3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 4, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 3],
    [3, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 3],
    [3, 0, 0, 1, 0, 3, 0, 0, 0, 1, 1, 0, 0, 3, 1, 1, 1, 1, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 3],
    [3, 0, 0, 4, 4, 4, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 3],
    [3, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 3],
    [3, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

# Solid tiles that player cannot walk through
SOLID_TILES = {TILE_TREE, TILE_WATER}
STARTER_NAMES = ["treecko", "torchic", "mudkip"]
WILD_POKEMON = ["poochyena", "zigzagoon", "wurmple", "taillow", "shroomish", "wingull", "geodude", "zubat", "makuhita", "tentacool"]
EVENT_POKEMON = STARTER_NAMES + WILD_POKEMON
EVOLUTION_LEVELS = {
    "treecko": (16, "grovyle"),
    "grovyle": (36, "sceptile"),
    "torchic": (16, "combusken"),
    "combusken": (36, "blaziken"),
    "mudkip": (16, "marshtomp"),
    "marshtomp": (36, "swampert"),
    "poochyena": (18, "mightyena"),
}
EVOLUTION_ITEMS = {
    "Leaf Stone": {"treecko": "grovyle", "grovyle": "sceptile"},
    "Fire Stone": {"torchic": "combusken", "combusken": "blaziken"},
    "Water Stone": {"mudkip": "marshtomp", "marshtomp": "swampert"},
    "Moon Stone": {"poochyena": "mightyena"},
}
STONE_FIND_SOURCES = {
    ("building", "home"): "Leaf Stone",
    ("building", "shore"): "Water Stone",
    ("building", "lab"): "Fire Stone",
    ("region", "Meteor Falls"): "Moon Stone",
}
ROUTE_ASSIST_TILE = (10, 1)
STARTER_MOVES = {
    "treecko": [
        {"name": "Pound", "power": 6, "accuracy": 95},
        {"name": "Absorb", "power": 7, "accuracy": 100, "drain": 0.5},
        {"name": "Quick Attack", "power": 5, "accuracy": 100},
        {"name": "Leer", "power": 3, "accuracy": 100},
    ],
    "torchic": [
        {"name": "Scratch", "power": 6, "accuracy": 100},
        {"name": "Ember", "power": 8, "accuracy": 95},
        {"name": "Quick Attack", "power": 5, "accuracy": 100},
        {"name": "Growl", "power": 3, "accuracy": 100},
    ],
    "mudkip": [
        {"name": "Tackle", "power": 6, "accuracy": 95},
        {"name": "Water Gun", "power": 8, "accuracy": 95},
        {"name": "Mud-Slap", "power": 5, "accuracy": 85},
        {"name": "Growl", "power": 3, "accuracy": 100},
    ],
}
BUILDINGS = [
    {
        "id": "home",
        "name": "Bluebell House",
        "kind": "house",
        "x": 2,
        "y": 3,
        "w": 4,
        "h": 3,
        "door": (3, 6),
        "roof": (226, 102, 102),
        "message": ["A cozy village home.", "Someone packed snacks for your trip."],
    },
    {
        "id": "lab",
        "name": "Professor's Lab",
        "kind": "lab",
        "x": 8,
        "y": 2,
        "w": 5,
        "h": 3,
        "door": (10, 5),
        "roof": BUILDING_ROOF,
        "message": ["Professor Birch left in a hurry.", "Pick a starter before heading north!"],
    },
    {
        "id": "shore",
        "name": "Shore House",
        "kind": "house",
        "x": 14,
        "y": 4,
        "w": 4,
        "h": 3,
        "door": (15, 7),
        "roof": (99, 188, 136),
        "message": ["The sea breeze rolls through town.", "A neighbor says the professor went north."],
    },
]
BUILDING_TILES = {
    (tile_x, tile_y)
    for building in BUILDINGS
    for tile_y in range(building["y"], building["y"] + building["h"])
    for tile_x in range(building["x"], building["x"] + building["w"])
}
REGION_STOPS = [
    {
        "name": "Oldale Town",
        "kind": "town",
        "subtitle": "A quiet stop north of Bluebell.",
        "lines": ["A clerk shows you the Pokemon Center.", "A rival waits near Route 103."],
    },
    {
        "name": "Route 103",
        "kind": "route",
        "subtitle": "Rival Battle",
        "lines": ["Your rival tests your new partner.", "After the battle, head home to report in."],
    },
    {
        "name": "Route 102",
        "kind": "route",
        "subtitle": "Trainer Road",
        "lines": ["Young trainers line the flowered path.", "The road bends west toward Petalburg."],
    },
    {
        "name": "Petalburg City",
        "kind": "town",
        "subtitle": "Your father's gym town.",
        "lines": ["The Gym Leader is busy training challengers.", "A new friend learns how to catch Pokemon."],
    },
    {
        "name": "Petalburg Woods",
        "kind": "forest",
        "subtitle": "A shady forest route.",
        "lines": ["A researcher is cornered by Team Tide.", "You chase the troublemakers toward Rustboro."],
    },
    {
        "name": "Rustboro City",
        "kind": "gym",
        "subtitle": "Rock Gym Challenge",
        "badge": "Stone Badge",
        "lines": ["The first gym tests sturdy defenses.", "Win here to prove your journey has begun."],
    },
    {
        "name": "Rusturf Tunnel",
        "kind": "cave",
        "subtitle": "Rescue Mission",
        "lines": ["Team Tide stole important goods.", "Follow them through the tunnel and recover the package."],
    },
    {
        "name": "Dewford Town",
        "kind": "gym",
        "subtitle": "Fighting Gym Challenge",
        "badge": "Knuckle Badge",
        "lines": ["A boat carries you over the southern sea.", "The island gym waits beyond the beach."],
    },
    {
        "name": "Granite Cave",
        "kind": "cave",
        "subtitle": "Letter Delivery",
        "lines": ["Deep in the cave, a quiet trainer studies rare stones.", "Deliver the letter before sailing onward."],
    },
    {
        "name": "Slateport City",
        "kind": "town",
        "subtitle": "Harbor Story",
        "lines": ["The museum is packed with Team Tide grunts.", "Protect the sea charts and head north."],
    },
    {
        "name": "Mauville City",
        "kind": "gym",
        "subtitle": "Electric Gym Challenge",
        "badge": "Dynamo Badge",
        "lines": ["A bright city hums with power.", "The gym is full of switches and electric traps."],
    },
    {
        "name": "Verdanturf Town",
        "kind": "town",
        "subtitle": "Quiet Valley",
        "lines": ["Flowers sway in the clean mountain air.", "The tunnel project reconnects old friends."],
    },
    {
        "name": "Fiery Path",
        "kind": "route",
        "subtitle": "Ash Road",
        "lines": ["The road climbs through smoke and warm stone.", "Team Tide is searching near Meteor Falls."],
    },
    {
        "name": "Meteor Falls",
        "kind": "cave",
        "subtitle": "Villain Plot",
        "lines": ["A stolen meteorite points toward the volcano.", "Follow the trail up Mt. Chimney."],
    },
    {
        "name": "Lavaridge Town",
        "kind": "gym",
        "subtitle": "Fire Gym Challenge",
        "badge": "Heat Badge",
        "lines": ["Hot springs steam behind the ridge.", "A heated gym battle waits inside."],
    },
    {
        "name": "Petalburg Gym",
        "kind": "gym",
        "subtitle": "Family Gym Challenge",
        "badge": "Balance Badge",
        "lines": ["With four badges, your father accepts your challenge.", "This battle measures how far you have come."],
    },
    {
        "name": "Weather Institute",
        "kind": "route",
        "subtitle": "Rain Route Rescue",
        "lines": ["Tall grass and bridges stretch through heavy rain.", "Team Tide storms the Weather Institute."],
    },
    {
        "name": "Fortree City",
        "kind": "gym",
        "subtitle": "Flying Gym Challenge",
        "badge": "Feather Badge",
        "lines": ["Treehouses rise above the forest canopy.", "The gym turns with wind and clever paths."],
    },
    {
        "name": "Lilycove City",
        "kind": "town",
        "subtitle": "Hideout Lead",
        "lines": ["The coast opens into a busy seaside city.", "Team Tide's hideout blocks the eastern water."],
    },
    {
        "name": "Mt. Pyre",
        "kind": "cave",
        "subtitle": "Ancient Orb Story",
        "lines": ["A sacred mountain reveals the villains' plan.", "The sea begins to churn with old power."],
    },
    {
        "name": "Mossdeep City",
        "kind": "gym",
        "subtitle": "Psychic Gym Challenge",
        "badge": "Mind Badge",
        "lines": ["The space center watches the stars.", "Twin leaders challenge you with a double battle."],
    },
    {
        "name": "Seafloor Cavern",
        "kind": "cave",
        "subtitle": "Deep Sea Crisis",
        "lines": ["Dive beneath the waves to find Team Tide.", "An ancient Pokemon wakes below the sea."],
    },
    {
        "name": "Sootopolis City",
        "kind": "gym",
        "subtitle": "Water Gym Challenge",
        "badge": "Rain Badge",
        "lines": ["A crater city surrounds a shining lake.", "Calm the crisis, then face the final gym."],
    },
    {
        "name": "Victory Road",
        "kind": "cave",
        "subtitle": "Final Trial",
        "lines": ["Every badge opens the path to the League.", "Strong trainers wait in the cavern ahead."],
    },
    {
        "name": "Pokemon League",
        "kind": "league",
        "subtitle": "Champion Challenge",
        "lines": ["The Elite Four stand between you and the title.", "Your Sapphire-style journey reaches its finale."],
    },
]
REGION_NODE_POSITIONS = [
    (402, 448),  # Oldale Town
    (402, 370),  # Route 103
    (300, 370),  # Route 102
    (196, 370),  # Petalburg City
    (164, 292),  # Petalburg Woods
    (238, 226),  # Rustboro City
    (330, 226),  # Rusturf Tunnel
    (108, 474),  # Dewford Town
    (178, 510),  # Granite Cave
    (330, 474),  # Slateport City
    (430, 392),  # Mauville City
    (338, 326),  # Verdanturf Town
    (520, 324),  # Fiery Path
    (596, 260),  # Meteor Falls
    (570, 180),  # Lavaridge Town
    (198, 440),  # Petalburg Gym
    (590, 372),  # Weather Institute
    (642, 292),  # Fortree City
    (694, 358),  # Lilycove City
    (628, 440),  # Mt. Pyre
    (704, 486),  # Mossdeep City
    (604, 520),  # Seafloor Cavern
    (522, 506),  # Sootopolis City
    (654, 136),  # Victory Road
    (724, 92),   # Pokemon League
]
REGION_ROUTE_LINKS = [
    (0, 1), (0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 15),
    (6, 11), (7, 8), (7, 9), (9, 10), (10, 11), (10, 12),
    (12, 13), (13, 14), (10, 16), (16, 17), (17, 18), (18, 19),
    (18, 20), (19, 21), (20, 21), (21, 22), (22, 23), (23, 24),
]
REGION_LINK_LOOKUP = {index: set() for index in range(len(REGION_STOPS))}
for start, end in REGION_ROUTE_LINKS:
    REGION_LINK_LOOKUP[start].add(end)
    REGION_LINK_LOOKUP[end].add(start)


def load_pokedex_names():
    img_dir = Path(__file__).resolve().parent / "Pokemon" / "img"
    if img_dir.exists():
        names = {path.stem.lower() for path in img_dir.glob("*.png")}
        if names:
            return sorted(names)
    return sorted(POKEDEX_FALLBACK)


def build_pokedex_knowledge(name, dex_number):
    habitats = ["forest edge", "rocky pass", "coastal shallows", "city outskirts", "mountain trail"]
    temperaments = ["calm", "bold", "curious", "fierce", "playful"]
    traits = ["quick reflexes", "strong instincts", "high stamina", "keen senses", "surprising agility"]
    habitat = habitats[dex_number % len(habitats)]
    temperament = temperaments[(dex_number + 2) % len(temperaments)]
    trait = traits[(dex_number + 4) % len(traits)]
    cap = name.capitalize()
    return [
        f"{cap} is often spotted near the {habitat}.",
        f"Trainers describe its behavior as {temperament}.",
        f"Field notes mention {trait} in battle.",
    ]


def build_pokedex_battle_profile(name, dex_number):
    move_pool = [
        "Tackle", "Quick Attack", "Bite", "Scratch", "Ember", "Water Gun",
        "Vine Whip", "Thunder Shock", "Rock Throw", "Wing Attack", "Confusion",
        "Ice Shard", "Shadow Sneak", "Mud-Slap", "Swift", "Headbutt",
    ]
    key = sum(ord(ch) for ch in name) + dex_number * 17
    hp = 45 + (key % 75)
    attack = 30 + ((key * 3) % 70)
    defense = 30 + ((key * 5) % 70)
    speed = 25 + ((key * 7) % 95)
    base_accuracy = 82 + (key % 16)

    moves = []
    for idx in range(4):
        move_name = move_pool[(key + idx * 5) % len(move_pool)]
        power = 35 + ((key + idx * 11) % 66)
        accuracy = min(100, max(70, base_accuracy - idx + (idx % 2)))
        moves.append({"name": move_name, "power": power, "accuracy": accuracy})
    return {
        "hp": hp,
        "attack": attack,
        "defense": defense,
        "speed": speed,
        "moves": moves,
    }


def load_species_profiles():
    """Parse local Pokemon class files for canonical HP and move sets."""
    profiles = {}
    pokemon_dir = Path(__file__).resolve().parent / "Pokemon" / "Pokemons"
    if not pokemon_dir.exists():
        return profiles

    py_files = sorted(pokemon_dir.glob("*.py"))
    class_start = re.compile(r"^\s*class\s+([A-Za-z0-9_]+)\s*\(")
    move_line = re.compile(r'Move\("([^"]+)",\s*"[^"]+",\s*([0-9]+)\)')
    hp_line = re.compile(r'super\(\)\.__init__\("([^"]+)",\s*([0-9]+),')

    for file_path in py_files:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lines):
            class_match = class_start.match(lines[i])
            if not class_match:
                i += 1
                continue

            class_indent = len(lines[i]) - len(lines[i].lstrip())
            class_name = class_match.group(1).lower()
            i += 1
            moves = []
            hp = None
            display_name = class_name

            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if stripped:
                    indent = len(line) - len(line.lstrip())
                    if indent <= class_indent and stripped.startswith("class "):
                        break
                move_match = move_line.search(line)
                if move_match:
                    moves.append({"name": move_match.group(1), "power": int(move_match.group(2))})
                hp_match = hp_line.search(line)
                if hp_match:
                    display_name = hp_match.group(1).lower()
                    hp = int(hp_match.group(2))
                i += 1

            if hp is not None and moves:
                key = display_name or class_name
                profiles[key] = {"hp": hp, "moves": moves[:4]}
        # continue outer while if class loop consumed file
    return profiles


class Game:
    def __init__(self):
        self.fullscreen = True
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beta Blue Version")
        self.clock = pygame.time.Clock()
        
        self.state = STATE_TITLE
        self.player_name = ""
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Player position (in tiles)
        self.player_x = 10
        self.player_y = 7
        
        # Player animation
        self.player_direction = "down"
        self.player_anim_frame = 0
        self.player_anim_timer = 0
        
        # Title screen animation
        self.title_timer = 0
        
        # Input handling
        self.name_input_active = True
        self.pokemon_sprites = self.load_pokemon_sprites()
        self.event_step = 0
        self.starter_choice = 0
        self.starter_name = None
        self.starter_level = 5
        self.professor_rescued = False
        self.trail_unlocked = False
        self.region_index = 0
        self.badges = []
        self.current_building = None
        self.player_max_hp = 22
        self.wild_max_hp = 18
        self.player_battle_hp = 22
        self.wild_battle_hp = 18
        self.selected_move = 0
        self.battle_message = ""
        self.floating_texts = []
        self.show_bag = False
        self.show_pokedex = False
        self.bag_items = {item_name: 0 for item_name in EVOLUTION_ITEMS}
        self.bag_items["Potion"] = 5
        self.bag_items["Poke Ball"] = 8
        self.bag_selection = 0
        self.menu_message = ""
        self.menu_message_timer = 0
        self.pokedex_names = load_pokedex_names()
        self.discovered_pokemon = set()
        self.pokedex_selection = 0
        self.pokedex_sprites = self.load_pokedex_sprites()
        self.species_profiles = load_species_profiles()
        self.found_sources = set()
        self.route_map = None
        self.route_player_x = 10
        self.route_player_y = 13
        self.wild_encounter_name = None
        self.wild_encounter_level = 2
        self.previous_state = STATE_ROUTE_EXPLORE
        self.test_region_index = 0
        self.test_region_scroll = 0
        self.active_wild_name = "poochyena"
        self.active_wild_level = self.starter_level + 1
        self.in_wild_battle = False
        self.battle_intro_timer = 0
        self.battle_intro_total = 70
        self.party_pokemon = []
        self.active_party_index = 0
        self.selected_battle_action = 0
        self.battle_submenu = "main"
        self.battle_bag_selection = 0
        self.battle_party_selection = 0
        self.attack_anim_timer = 0
        self.attack_anim_total = 0
        self.attack_anim_move = ""
        self.attack_anim_target = "wild"
        self.attack_anim_from = "player"

    def toggle_fullscreen(self):
        """Switch between fullscreen and a normal 800x600 window."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def present_screen(self):
        """Scale the fixed game canvas to the current window."""
        window_width, window_height = self.window.get_size()
        pygame.transform.scale(self.screen, (window_width, window_height), self.window)
        pygame.display.flip()

    def load_pokemon_sprites(self):
        """Load small Pokemon sprites from the local asset folder for story events."""
        sprites = {}
        img_dir = Path(__file__).resolve().parent / "Pokemon" / "img"
        for name in EVENT_POKEMON:
            path = img_dir / f"{name}.png"
            if path.exists():
                image = pygame.image.load(path).convert_alpha()
                sprites[name] = self.scale_sprite(image, 42)
        return sprites

    def load_pokedex_sprites(self):
        sprites = {}
        img_dir = Path(__file__).resolve().parent / "Pokemon" / "img"
        for name in self.pokedex_names:
            path = img_dir / f"{name}.png"
            if path.exists():
                image = pygame.image.load(path).convert_alpha()
                sprites[name] = self.scale_sprite(image, 160)
        return sprites

    def scale_sprite(self, image, max_size):
        """Scale sprites up only enough to stay readable without dominating the scene."""
        width, height = image.get_size()
        scale = min(max_size / width, max_size / height)
        scale = max(1, scale)
        new_size = (int(width * scale), int(height * scale))
        return pygame.transform.scale(image, new_size)

    def draw_rounded_rect(self, rect, color, radius=8, outline_color=None, outline_width=3):
        """Draw a rounded rectangle with a bold handheld-style outline."""
        if outline_color and outline_width > 0:
            pygame.draw.rect(self.screen, outline_color, rect, border_radius=radius)
            inner = rect.inflate(-outline_width * 2, -outline_width * 2)
            pygame.draw.rect(self.screen, color, inner, border_radius=max(1, radius - outline_width))
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def draw_gba_panel(self, rect, color=UI_PANEL):
        """Draw a crisp blue-bordered panel inspired by GBA RPG text boxes."""
        pygame.draw.rect(self.screen, GBA_PANEL_BLUE, rect, border_radius=4)
        pygame.draw.rect(self.screen, GBA_PANEL_SHADOW, rect.inflate(-6, -6), border_radius=3)
        pygame.draw.rect(self.screen, color, rect.inflate(-10, -10), border_radius=2)

    def wrap_text_to_width(self, text, font, max_width):
        words = text.split()
        if not words:
            return [""]
        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def draw_text_block(self, lines, x, y, max_width, line_height=22, color=OUTLINE):
        draw_y = y
        for line in lines:
            wrapped = self.wrap_text_to_width(line, self.font_small, max_width)
            for wrapped_line in wrapped:
                text = self.font_small.render(wrapped_line, True, color)
                self.screen.blit(text, (x, draw_y))
                draw_y += line_height
        return draw_y

    def fit_text_single_line(self, text, font, max_width):
        if font.size(text)[0] <= max_width:
            return text
        ellipsis = "..."
        trimmed = text
        while trimmed and font.size(trimmed + ellipsis)[0] > max_width:
            trimmed = trimmed[:-1]
        return (trimmed + ellipsis) if trimmed else ellipsis
        
    def is_solid(self, x, y):
        """Check if a tile is solid"""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return True
        return (x, y) in BUILDING_TILES or TOWN_MAP[y][x] in SOLID_TILES

    def get_building_at_player(self):
        for building in BUILDINGS:
            if (self.player_x, self.player_y) == building["door"]:
                return building
        return None

    def player_at_route_assist(self):
        return (self.player_x, self.player_y) == ROUTE_ASSIST_TILE
    
    def draw_tile(self, x, y, tile_type):
        """Draw a single tile"""
        pixel_x = MAP_OFFSET_X + x * TILE_SIZE
        pixel_y = MAP_OFFSET_Y + y * TILE_SIZE
        
        if tile_type == TILE_GRASS:
            color = GRASS if (x + y) % 2 == 0 else GRASS_LIGHT
            pygame.draw.rect(self.screen, color, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, (91, 190, 106), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 1)
            if (x * 3 + y * 7) % 5 == 0:
                pygame.draw.line(self.screen, GRASS_DARK, (pixel_x + 8, pixel_y + 22), (pixel_x + 10, pixel_y + 16), 2)
                pygame.draw.line(self.screen, GRASS_DARK, (pixel_x + 22, pixel_y + 18), (pixel_x + 25, pixel_y + 12), 2)
            if (x * 5 + y * 2) % 13 == 0:
                pygame.draw.circle(self.screen, FLOWER_PINK, (pixel_x + 12, pixel_y + 12), 2)
                pygame.draw.circle(self.screen, FLOWER_YELLOW, (pixel_x + 21, pixel_y + 22), 2)
                
        elif tile_type == TILE_PATH:
            pygame.draw.rect(self.screen, PATH, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, PATH_LIGHT, (pixel_x + 3, pixel_y + 3, 26, 26), 1, border_radius=4)
            if (x + y) % 2 == 0:
                pygame.draw.circle(self.screen, PATH_DARK, (pixel_x + 9, pixel_y + 21), 2)
                pygame.draw.circle(self.screen, PATH_DARK, (pixel_x + 23, pixel_y + 10), 1)
            
        elif tile_type == TILE_BUILDING:
            self.draw_rounded_rect(
                pygame.Rect(pixel_x + 1, pixel_y + 6, TILE_SIZE - 2, TILE_SIZE - 7),
                BUILDING,
                radius=7,
                outline_color=OUTLINE,
                outline_width=2,
            )
            self.draw_rounded_rect(
                pygame.Rect(pixel_x + 2, pixel_y + 1, TILE_SIZE - 4, 14),
                BUILDING_ROOF,
                radius=6,
                outline_color=OUTLINE,
                outline_width=2,
            )
            pygame.draw.rect(self.screen, BUILDING_ROOF_DARK, (pixel_x + 6, pixel_y + 10, 20, 4), border_radius=2)
            pygame.draw.rect(self.screen, BUILDING_SHADE, (pixel_x + 5, pixel_y + 18, 8, 6), border_radius=2)
            pygame.draw.rect(self.screen, (115, 75, 54), (pixel_x + 18, pixel_y + 17, 8, 13), border_radius=3)
            pygame.draw.circle(self.screen, TEXT_GOLD, (pixel_x + 24, pixel_y + 24), 1)
            
        elif tile_type == TILE_TREE:
            pygame.draw.rect(self.screen, TREE_TRUNK, (pixel_x + 12, pixel_y + 19, 8, 13), border_radius=3)
            pygame.draw.circle(self.screen, OUTLINE, (pixel_x + 16, pixel_y + 13), 15)
            pygame.draw.circle(self.screen, TREE, (pixel_x + 16, pixel_y + 13), 13)
            pygame.draw.circle(self.screen, TREE_LIGHT, (pixel_x + 10, pixel_y + 8), 6)
            pygame.draw.circle(self.screen, TREE_DARK, (pixel_x + 22, pixel_y + 16), 7)
            
        elif tile_type == TILE_WATER:
            pygame.draw.rect(self.screen, WATER, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, WATER_DARK, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 1)
            wave_shift = (pygame.time.get_ticks() // 250 + x + y) % 4
            pygame.draw.line(self.screen, WATER_LIGHT, (pixel_x + 4 + wave_shift, pixel_y + 9), (pixel_x + 15 + wave_shift, pixel_y + 9), 2)
            pygame.draw.line(self.screen, WATER_LIGHT, (pixel_x + 15 - wave_shift, pixel_y + 22), (pixel_x + 28 - wave_shift, pixel_y + 22), 2)

        elif tile_type == TILE_TALL_GRASS:
            pygame.draw.rect(self.screen, GRASS, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, (78, 176, 94), (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 1)
            for blade_x in range(5, TILE_SIZE, 7):
                sway = ((pygame.time.get_ticks() // 240) + x + blade_x) % 3
                pygame.draw.line(
                    self.screen,
                    GRASS_DARK,
                    (pixel_x + blade_x, pixel_y + 26),
                    (pixel_x + blade_x + sway - 1, pixel_y + 11),
                    3,
                )
            if (x * 7 + y * 5) % 6 == 0:
                pygame.draw.circle(self.screen, FLOWER_YELLOW, (pixel_x + 24, pixel_y + 10), 2)

    def draw_building(self, building):
        """Draw one enterable building as a single readable landmark."""
        x = MAP_OFFSET_X + building["x"] * TILE_SIZE
        y = MAP_OFFSET_Y + building["y"] * TILE_SIZE
        width = building["w"] * TILE_SIZE
        height = building["h"] * TILE_SIZE
        pygame.draw.ellipse(self.screen, (52, 128, 92), (x + 8, y + height - 8, width - 16, 14))
        self.draw_rounded_rect(
            pygame.Rect(x + 4, y + 28, width - 8, height - 32),
            BUILDING,
            radius=12,
            outline_color=OUTLINE,
            outline_width=3,
        )
        pygame.draw.polygon(
            self.screen,
            OUTLINE,
            [(x - 2, y + 35), (x + width // 2, y), (x + width + 2, y + 35)],
        )
        pygame.draw.polygon(
            self.screen,
            building["roof"],
            [(x + 5, y + 34), (x + width // 2, y + 7), (x + width - 5, y + 34)],
        )
        pygame.draw.line(self.screen, BUILDING_ROOF_DARK, (x + 16, y + 36), (x + width - 16, y + 36), 4)
        door_x = MAP_OFFSET_X + building["door"][0] * TILE_SIZE + 6
        door_y = MAP_OFFSET_Y + building["door"][1] * TILE_SIZE - 30
        pygame.draw.rect(self.screen, (126, 84, 58), (door_x, door_y, 20, 34), border_radius=5)
        pygame.draw.circle(self.screen, TEXT_GOLD, (door_x + 15, door_y + 18), 2)
        pygame.draw.rect(self.screen, (173, 225, 250), (x + 20, y + 56, 20, 16), border_radius=4)
        pygame.draw.rect(self.screen, OUTLINE, (x + 20, y + 56, 20, 16), 2, border_radius=4)
        pygame.draw.rect(self.screen, (173, 225, 250), (x + width - 40, y + 56, 20, 16), border_radius=4)
        pygame.draw.rect(self.screen, OUTLINE, (x + width - 40, y + 56, 20, 16), 2, border_radius=4)

        label = self.font_small.render(building["name"], True, OUTLINE)
        label_rect = label.get_rect(center=(x + width // 2, y + height + 13))
        pygame.draw.rect(self.screen, UI_PANEL, label_rect.inflate(8, 4), border_radius=4)
        self.screen.blit(label, label_rect)

    def draw_dialog_box(self, lines, prompt="Press ENTER"):
        box = pygame.Rect(54, SCREEN_HEIGHT - 142, SCREEN_WIDTH - 108, 104)
        self.draw_gba_panel(box)
        for index, line in enumerate(lines):
            text = self.font_medium.render(line, True, OUTLINE)
            self.screen.blit(text, (box.x + 24, box.y + 18 + index * 28))
        prompt_text = self.font_small.render(prompt, True, TEXT_BLUE)
        prompt_rect = prompt_text.get_rect(right=box.right - 24, bottom=box.bottom - 14)
        self.screen.blit(prompt_text, prompt_rect)

    def discover_pokemon(self, pokemon_name):
        if not pokemon_name:
            return
        self.discovered_pokemon.add(pokemon_name.lower())

    def try_find_stone(self, source_kind, source_id):
        source_key = (source_kind, source_id)
        if source_key in self.found_sources:
            return
        stone_name = STONE_FIND_SOURCES.get(source_key)
        if not stone_name:
            return
        self.found_sources.add(source_key)
        self.bag_items[stone_name] += 1
        self.menu_message = f"You found a {stone_name}!"
        self.menu_message_timer = 240

    def set_menu_message(self, text, timer=180):
        self.menu_message = text
        self.menu_message_timer = timer

    def get_bag_item_names(self):
        return list(self.bag_items.keys())

    def use_selected_bag_item(self):
        item_names = self.get_bag_item_names()
        if not item_names:
            self.set_menu_message("Your bag is empty.")
            return
        item_name = item_names[self.bag_selection]
        if self.bag_items[item_name] <= 0:
            self.set_menu_message(f"No {item_name} left.")
            return
        if not self.starter_name:
            self.set_menu_message("You do not have a Pokemon yet.")
            return
        evolution_targets = EVOLUTION_ITEMS[item_name]
        current_name = self.starter_name.lower()
        evolved_name = evolution_targets.get(current_name)
        if not evolved_name:
            self.set_menu_message(f"{item_name} has no effect on {self.starter_name.capitalize()}.")
            return
        self.starter_name = evolved_name
        self.bag_items[item_name] -= 1
        self.discover_pokemon(self.starter_name)
        if self.party_pokemon:
            self.party_pokemon[0] = self.starter_name
        self.set_menu_message(f"{current_name.capitalize()} evolved into {evolved_name.capitalize()}!")

    def draw_menu_message(self):
        if self.menu_message_timer <= 0 or not self.menu_message:
            return
        self.menu_message_timer -= 1
        msg_panel = pygame.Rect(170, 18, SCREEN_WIDTH - 340, 42)
        self.draw_rounded_rect(msg_panel, (255, 250, 217), radius=8, outline_color=OUTLINE, outline_width=2)
        msg_text = self.font_small.render(self.menu_message, True, OUTLINE)
        msg_rect = msg_text.get_rect(center=msg_panel.center)
        self.screen.blit(msg_text, msg_rect)

    def draw_bag_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(165)
        overlay.fill((9, 34, 74))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(96, 68, SCREEN_WIDTH - 192, SCREEN_HEIGHT - 136)
        self.draw_rounded_rect(panel, UI_PANEL, radius=16, outline_color=OUTLINE, outline_width=4)
        title = self.font_large.render("Bag", True, TEXT_BLUE)
        self.screen.blit(title, (panel.x + 24, panel.y + 18))

        item_names = self.get_bag_item_names()
        if self.bag_selection >= len(item_names):
            self.bag_selection = max(0, len(item_names) - 1)
        for index, item_name in enumerate(item_names):
            line_rect = pygame.Rect(panel.x + 24, panel.y + 74 + index * 42, panel.width - 48, 34)
            selected = index == self.bag_selection
            line_color = (255, 248, 207) if selected else (233, 244, 255)
            line_outline = TEXT_GOLD if selected else OUTLINE
            self.draw_rounded_rect(line_rect, line_color, radius=8, outline_color=line_outline, outline_width=2)
            label = self.font_small.render(f"{item_name} x{self.bag_items[item_name]}", True, OUTLINE)
            self.screen.blit(label, (line_rect.x + 12, line_rect.y + 8))

        partner = self.starter_name.capitalize() if self.starter_name else "None"
        partner_text = self.font_small.render(f"Partner: {partner}", True, OUTLINE)
        self.screen.blit(partner_text, (panel.x + 24, panel.bottom - 92))
        help_text = self.font_small.render("UP/DOWN select  ENTER use item  B/ESC close", True, TEXT_BLUE)
        self.screen.blit(help_text, (panel.x + 24, panel.bottom - 62))
        if self.menu_message:
            msg = self.font_small.render(self.menu_message, True, OUTLINE)
            self.screen.blit(msg, (panel.x + 24, panel.bottom - 34))

    def draw_pokedex_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(165)
        overlay.fill((9, 34, 74))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(72, 40, SCREEN_WIDTH - 144, SCREEN_HEIGHT - 80)
        self.draw_rounded_rect(panel, UI_PANEL, radius=16, outline_color=OUTLINE, outline_width=4)
        found_count = len(self.discovered_pokemon)
        total_count = len(self.pokedex_names)
        title = self.font_large.render(f"Pokedex {found_count}/{total_count}", True, TEXT_BLUE)
        self.screen.blit(title, (panel.x + 24, panel.y + 18))
        if not self.pokedex_names:
            empty_text = self.font_medium.render("No Pokedex entries found.", True, OUTLINE)
            self.screen.blit(empty_text, (panel.x + 24, panel.y + 90))
            return

        self.pokedex_selection = max(0, min(self.pokedex_selection, total_count - 1))
        pokemon_name = self.pokedex_names[self.pokedex_selection]
        discovered = pokemon_name in self.discovered_pokemon
        dex_number = self.pokedex_selection + 1
        name_text = pokemon_name.capitalize() if discovered else "???"

        left_page = pygame.Rect(panel.x + 24, panel.y + 78, 250, panel.height - 124)
        right_page = pygame.Rect(panel.x + 290, panel.y + 78, panel.width - 314, panel.height - 124)
        self.draw_rounded_rect(left_page, (233, 244, 255), radius=10, outline_color=OUTLINE, outline_width=2)
        self.draw_rounded_rect(right_page, (255, 250, 217), radius=10, outline_color=OUTLINE, outline_width=2)

        dex_text = self.font_small.render(f"#{dex_number:03}", True, OUTLINE)
        self.screen.blit(dex_text, (left_page.x + 14, left_page.y + 12))
        species_text = self.font_medium.render(name_text, True, OUTLINE)
        self.screen.blit(species_text, (left_page.x + 14, left_page.y + 30))

        sprite = self.pokedex_sprites.get(pokemon_name)
        if discovered and sprite:
            sprite_rect = sprite.get_rect(center=(left_page.centerx, left_page.y + 170))
            self.screen.blit(sprite, sprite_rect)
        else:
            hidden = self.font_large.render("???", True, (118, 132, 148))
            hidden_rect = hidden.get_rect(center=(left_page.centerx, left_page.y + 160))
            self.screen.blit(hidden, hidden_rect)

        profile_title = self.font_small.render("Battle Profile", True, OUTLINE)
        self.screen.blit(profile_title, (left_page.x + 14, left_page.bottom - 150))
        if discovered:
            profile = self.species_profiles.get(pokemon_name)
            if profile:
                hp_value = profile["hp"]
                avg_power = sum(move["power"] for move in profile["moves"]) // max(1, len(profile["moves"]))
                accuracy_hint = max(80, 100 - (avg_power // 8))
                stats_line_1 = self.font_tiny.render(f"HP {hp_value}  PWR {avg_power}", True, OUTLINE)
                stats_line_2 = self.font_tiny.render(f"ACC {accuracy_hint}%  MOVES {len(profile['moves'])}", True, OUTLINE)
                self.screen.blit(stats_line_1, (left_page.x + 14, left_page.bottom - 124))
                self.screen.blit(stats_line_2, (left_page.x + 14, left_page.bottom - 106))
                moves_title = self.font_tiny.render("Moves (Power/Acc):", True, OUTLINE)
                self.screen.blit(moves_title, (left_page.x + 14, left_page.bottom - 88))
                move_y = left_page.bottom - 70
                max_move_width = left_page.width - 28
                for idx, move in enumerate(profile["moves"][:4]):
                    accuracy = max(70, 100 - (move["power"] // 6))
                    move_line = f"{idx + 1}. {move['name']}  P{move['power']} A{accuracy}%"
                    fitted_line = self.fit_text_single_line(move_line, self.font_tiny, max_move_width)
                    move_text = self.font_tiny.render(fitted_line, True, OUTLINE)
                    self.screen.blit(move_text, (left_page.x + 14, move_y))
                    move_y += 16
            else:
                fallback = build_pokedex_battle_profile(pokemon_name, dex_number)
                stats_line_1 = self.font_tiny.render(f"HP {fallback['hp']}  PWR ~{fallback['attack']}", True, OUTLINE)
                stats_line_2 = self.font_tiny.render("Move data unavailable in local dex files.", True, OUTLINE)
                self.screen.blit(stats_line_1, (left_page.x + 14, left_page.bottom - 124))
                self.screen.blit(stats_line_2, (left_page.x + 14, left_page.bottom - 104))
        else:
            locked_stats = self.font_small.render("Stats locked until discovered.", True, (118, 132, 148))
            self.screen.blit(locked_stats, (left_page.x + 14, left_page.bottom - 124))

        info_title = self.font_medium.render("Background Knowledge", True, OUTLINE)
        self.screen.blit(info_title, (right_page.x + 16, right_page.y + 12))
        if discovered:
            info_lines = build_pokedex_knowledge(pokemon_name, dex_number)
        else:
            info_lines = [
                "Entry locked.",
                "Discover this Pokemon in the world",
                "to unlock full field notes.",
            ]
        self.draw_text_block(
            info_lines,
            right_page.x + 16,
            right_page.y + 56,
            right_page.width - 32,
            line_height=24,
            color=OUTLINE if discovered else (118, 132, 148),
        )

        help_text = self.font_small.render("LEFT/RIGHT browse  P/ESC close", True, TEXT_BLUE)
        help_rect = help_text.get_rect(right=panel.right - 20, bottom=panel.bottom - 16)
        self.screen.blit(help_text, help_rect)

    def handle_menu_input(self, event):
        if event.key == pygame.K_b:
            self.show_bag = not self.show_bag
            if self.show_bag:
                self.show_pokedex = False
            return True
        if event.key == pygame.K_p:
            self.show_pokedex = not self.show_pokedex
            if self.show_pokedex:
                self.show_bag = False
            return True

        if self.show_bag:
            item_count = len(self.get_bag_item_names())
            if event.key in (pygame.K_ESCAPE,):
                self.show_bag = False
            elif event.key == pygame.K_UP and item_count > 0:
                self.bag_selection = (self.bag_selection - 1) % item_count
            elif event.key == pygame.K_DOWN and item_count > 0:
                self.bag_selection = (self.bag_selection + 1) % item_count
            elif event.key == pygame.K_RETURN:
                self.use_selected_bag_item()
            return True

        if self.show_pokedex:
            if event.key in (pygame.K_ESCAPE,):
                self.show_pokedex = False
            elif event.key == pygame.K_LEFT and self.pokedex_names:
                self.pokedex_selection = (self.pokedex_selection - 1) % len(self.pokedex_names)
            elif event.key == pygame.K_RIGHT and self.pokedex_names:
                self.pokedex_selection = (self.pokedex_selection + 1) % len(self.pokedex_names)
            return True
        return False
    
    def draw_player(self):
        """Draw the player character"""
        self.draw_player_at(self.player_x, self.player_y)

    def draw_player_at(self, tile_x, tile_y):
        """Draw the player character at a tile position."""
        pixel_x = MAP_OFFSET_X + tile_x * TILE_SIZE
        pixel_y = MAP_OFFSET_Y + tile_y * TILE_SIZE
        
        # Animation offset
        anim_offset = 0
        if self.player_anim_frame == 1:
            anim_offset = 2
        elif self.player_anim_frame == 2:
            anim_offset = -2
        
        # Body
        body_color = PLAYER_COLOR
        pygame.draw.ellipse(self.screen, (50, 90, 110), (pixel_x + 7, pixel_y + 26, 18, 6))
        pygame.draw.rect(self.screen, OUTLINE, (pixel_x + 7, pixel_y + 11 + anim_offset, 18, 15), border_radius=5)
        pygame.draw.rect(self.screen, body_color, (pixel_x + 9, pixel_y + 13 + anim_offset, 14, 11), border_radius=4)
        
        # Head
        pygame.draw.circle(self.screen, OUTLINE, (pixel_x + 16, pixel_y + 9 + anim_offset), 10)
        pygame.draw.circle(self.screen, (255, 207, 183), (pixel_x + 16, pixel_y + 9 + anim_offset), 8)
        
        # Hair
        pygame.draw.circle(self.screen, (105, 74, 54), (pixel_x + 16, pixel_y + 5 + anim_offset), 6)
        
        # Eyes based on direction
        eye_color = (50, 50, 50)
        if self.player_direction == "down":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 13, pixel_y + 10 + anim_offset), 2)
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 19, pixel_y + 10 + anim_offset), 2)
        elif self.player_direction == "up":
            pass  # No eyes visible from behind
        elif self.player_direction == "left":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 12, pixel_y + 10 + anim_offset), 2)
        elif self.player_direction == "right":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 20, pixel_y + 10 + anim_offset), 2)
        
        # Legs with animation
        leg_color = (50, 50, 150)
        if self.player_direction in ["down", "up"]:
            if self.player_anim_frame == 1:
                pygame.draw.rect(self.screen, leg_color, (pixel_x + 9, pixel_y + 24, 5, 8))
                pygame.draw.rect(self.screen, leg_color, (pixel_x + 18, pixel_y + 24, 5, 6))
            else:
                pygame.draw.rect(self.screen, leg_color, (pixel_x + 9, pixel_y + 24, 5, 6))
                pygame.draw.rect(self.screen, leg_color, (pixel_x + 18, pixel_y + 24, 5, 8))
        else:
            pygame.draw.rect(self.screen, leg_color, (pixel_x + 9, pixel_y + 24, 5, 8))
            pygame.draw.rect(self.screen, leg_color, (pixel_x + 18, pixel_y + 24, 5, 8))
    
    def draw_title_screen(self):
        """Draw the title screen"""
        # Background
        self.screen.fill(SAPPHIRE_MID)
        
        # Animated ocean-and-route pattern
        self.title_timer += 1
        pygame.draw.rect(self.screen, SAPPHIRE_DEEP, (0, 0, SCREEN_WIDTH, 330))
        pygame.draw.rect(self.screen, SAPPHIRE_MID, (0, 150, SCREEN_WIDTH, 180))
        pygame.draw.rect(self.screen, (114, 209, 128), (0, 360, SCREEN_WIDTH, 240))
        pygame.draw.rect(self.screen, PATH, (0, 420, SCREEN_WIDTH, 80))
        for i in range(-80, SCREEN_WIDTH + 80, 80):
            wave_y = 80 + ((i + self.title_timer) % 60)
            pygame.draw.arc(self.screen, SAPPHIRE_LIGHT, (i, wave_y, 72, 28), 0, 3.14, 3)
            pygame.draw.arc(self.screen, TEXT_WHITE, (i + 20, wave_y + 76, 72, 28), 0, 3.14, 2)
        
        # Title
        shadow = self.font_title.render("Beta Blue", True, OUTLINE)
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 88))
        self.screen.blit(shadow, shadow_rect)
        title_text = self.font_title.render("Beta Blue", True, TEXT_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 92))
        self.screen.blit(title_text, title_rect)

        version = self.font_large.render("VERSION", True, TEXT_WHITE)
        version_rect = version.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 42))
        self.screen.blit(version, version_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Hoenn-inspired shore adventure", True, TEXT_WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 8))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Start prompt (blinking)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start_text = self.font_large.render("PRESS START", True, TEXT_WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 82))
            self.screen.blit(start_text, start_rect)

        test_text = self.font_medium.render("Press T for Test Run", True, TEXT_GOLD)
        test_rect = test_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 132))
        self.screen.blit(test_text, test_rect)
        
        # Credits
        credits_text = self.font_small.render("Use Arrow Keys to Move  |  F11 Toggle Fullscreen", True, (238, 251, 255))
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(credits_text, credits_rect)

    def draw_test_region_picker(self):
        """Draw a developer menu for starting at any built region stop."""
        self.screen.fill(SAPPHIRE_DEEP)
        pygame.draw.rect(self.screen, (74, 151, 171), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.ellipse(self.screen, (112, 199, 138), (-86, 118, 520, 430))
        pygame.draw.ellipse(self.screen, (104, 189, 128), (364, 70, 500, 470))

        panel = pygame.Rect(92, 54, SCREEN_WIDTH - 184, SCREEN_HEIGHT - 108)
        self.draw_gba_panel(panel, (255, 250, 217))
        title = self.font_large.render("Test Run Start", True, OUTLINE)
        self.screen.blit(title, (panel.x + 28, panel.y + 22))
        subtitle = self.font_small.render("Pick any made region stop. ENTER jumps there, ESC returns.", True, TEXT_BLUE)
        self.screen.blit(subtitle, (panel.x + 30, panel.y + 64))

        visible_rows = 12
        if self.test_region_index < self.test_region_scroll:
            self.test_region_scroll = self.test_region_index
        elif self.test_region_index >= self.test_region_scroll + visible_rows:
            self.test_region_scroll = self.test_region_index - visible_rows + 1

        list_top = panel.y + 100
        for row in range(visible_rows):
            index = self.test_region_scroll + row
            if index >= len(REGION_STOPS):
                break
            stop = REGION_STOPS[index]
            item_rect = pygame.Rect(panel.x + 28, list_top + row * 32, panel.width - 56, 28)
            selected = index == self.test_region_index
            if selected:
                pygame.draw.rect(self.screen, TEXT_GOLD, item_rect, border_radius=5)
                pygame.draw.rect(self.screen, OUTLINE, item_rect, 2, border_radius=5)
            number = self.font_small.render(f"{index + 1:02}", True, TEXT_BLUE if not selected else OUTLINE)
            kind = self.font_small.render(stop["kind"].upper(), True, TEXT_BLUE if not selected else OUTLINE)
            name = self.font_small.render(stop["name"], True, OUTLINE)
            subtitle_text = self.font_small.render(stop["subtitle"], True, TEXT_BLUE if not selected else OUTLINE)
            self.screen.blit(number, (item_rect.x + 10, item_rect.y + 6))
            self.screen.blit(kind, (item_rect.x + 58, item_rect.y + 6))
            self.screen.blit(name, (item_rect.x + 154, item_rect.y + 6))
            self.screen.blit(subtitle_text, (item_rect.x + 350, item_rect.y + 6))

        footer = self.font_small.render("UP/DOWN: choose  PAGE UP/DOWN: jump  ENTER: start testing", True, TEXT_BLUE)
        footer_rect = footer.get_rect(center=(SCREEN_WIDTH // 2, panel.bottom - 26))
        self.screen.blit(footer, footer_rect)
    
    def draw_name_entry_screen(self):
        """Draw the name entry screen"""
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((9, 34, 74))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 105, 460, 225)
        self.draw_rounded_rect(panel, UI_PANEL, radius=16, outline_color=OUTLINE, outline_width=4)
        
        # Prompt
        prompt = self.font_large.render("Enter Your Name:", True, TEXT_BLUE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(prompt, prompt_rect)
        
        # Name input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        pygame.draw.rect(self.screen, (233, 244, 255), input_box, border_radius=8)
        pygame.draw.rect(self.screen, TEXT_GOLD, input_box, 3, border_radius=8)
        
        # Display entered name
        name_text = self.font_large.render(self.player_name, True, OUTLINE)
        name_rect = name_text.get_rect(center=input_box.center)
        self.screen.blit(name_text, name_rect)
        
        # Cursor
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = name_rect.right + 5
            pygame.draw.line(self.screen, OUTLINE, (cursor_x, name_rect.top), (cursor_x, name_rect.bottom), 2)
        
        # Instructions
        if len(self.player_name) > 0:
            instruction = self.font_medium.render("Press ENTER to confirm", True, TEXT_BLUE)
        else:
            instruction = self.font_medium.render("Type your name", True, TEXT_BLUE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_town(self):
        """Draw the town map"""
        # Draw all tiles
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                self.draw_tile(x, y, TOWN_MAP[y][x])
        
        for building in BUILDINGS:
            self.draw_building(building)

        route_sign = pygame.Rect(MAP_OFFSET_X + 348, MAP_OFFSET_Y + 50, 104, 32)
        self.draw_gba_panel(route_sign, (255, 250, 217))
        sign_text = self.font_small.render("ROUTE 101", True, OUTLINE)
        sign_rect = sign_text.get_rect(center=route_sign.center)
        self.screen.blit(sign_text, sign_rect)

        # Draw player
        self.draw_player()

        building = self.get_building_at_player()
        if building:
            self.draw_dialog_box([f"Enter {building['name']}?", "Press ENTER to go inside."], "ENTER")
        elif self.player_at_route_assist() and not self.professor_rescued:
            self.draw_dialog_box(["You hear the professor shouting up ahead!", "Press ENTER to enter the north trail."], "ENTER")
        elif self.player_at_route_assist() and self.trail_unlocked:
            self.draw_dialog_box(["The north trail opens onto connected routes.", "Press ENTER to travel the region."], "ENTER")
        elif self.player_at_route_assist() and self.professor_rescued:
            starter = self.starter_name.capitalize() if self.starter_name else "starter"
            self.draw_dialog_box([f"The northern route is calm again.", f"Visit the lab with {starter} first."], "ENTER")
        
        # Draw player name above player
        if self.player_name:
            name_label = self.font_small.render(self.player_name, True, TEXT_WHITE)
            label_x = MAP_OFFSET_X + self.player_x * TILE_SIZE + TILE_SIZE // 2
            label_y = MAP_OFFSET_Y + self.player_y * TILE_SIZE - 5
            label_rect = name_label.get_rect(center=(label_x, label_y))
            
            # Background for name
            bg_rect = label_rect.copy()
            bg_rect.inflate_ip(4, 2)
            pygame.draw.rect(self.screen, OUTLINE, bg_rect, border_radius=4)
            self.screen.blit(name_label, label_rect)
        hud_hint = self.font_small.render("B: Bag  P: Pokedex", True, TEXT_WHITE)
        self.screen.blit(hud_hint, (MAP_OFFSET_X + 6, MAP_OFFSET_Y + MAP_PIXEL_HEIGHT + 8))

    def draw_building_interior(self):
        """Draw simple interiors for homes and the professor's lab."""
        building = self.current_building or BUILDINGS[0]
        self.screen.fill((119, 194, 156))
        floor = pygame.Rect(84, 72, SCREEN_WIDTH - 168, SCREEN_HEIGHT - 196)
        floor_color = (244, 224, 167) if building["kind"] == "house" else (218, 236, 247)
        self.draw_rounded_rect(floor, floor_color, radius=18, outline_color=OUTLINE, outline_width=5)
        title = self.font_large.render(building["name"], True, OUTLINE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 116))
        self.screen.blit(title, title_rect)

        if building["kind"] == "lab":
            pygame.draw.rect(self.screen, (224, 174, 111), (124, 170, 196, 48), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (124, 170, 196, 48), 3, border_radius=8)
            pygame.draw.rect(self.screen, (166, 211, 234), (488, 158, 116, 138), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (488, 158, 116, 138), 3, border_radius=8)
            if not self.professor_rescued:
                self.draw_dialog_box(["Professor Birch rushed toward the north trail.", "His starter bag is missing from the lab!"], "ESC to leave")
            else:
                starter = self.starter_name.capitalize() if self.starter_name else "starter"
                self.draw_dialog_box([f"Professor Birch: Great work with {starter}!", "The north trail to the region map is open."], "ESC to leave")
        else:
            pygame.draw.rect(self.screen, (224, 174, 111), (134, 166, 170, 50), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (134, 166, 170, 50), 3, border_radius=8)
            pygame.draw.rect(self.screen, (126, 84, 58), (506, 150, 92, 130), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (506, 150, 92, 130), 3, border_radius=8)
            self.draw_dialog_box(building["message"], "ESC to leave")

    def draw_next_town(self):
        """Draw the open region map reached from the north trail."""
        stop = REGION_STOPS[self.region_index]
        self.screen.fill((116, 193, 156))
        pygame.draw.rect(self.screen, (74, 151, 171), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.ellipse(self.screen, (112, 199, 138), (-78, 82, 610, 500))
        pygame.draw.ellipse(self.screen, (104, 189, 128), (372, 42, 482, 500))
        pygame.draw.ellipse(self.screen, (83, 170, 116), (494, 250, 312, 280))
        pygame.draw.ellipse(self.screen, WATER, (516, 392, 220, 150))
        pygame.draw.ellipse(self.screen, WATER_LIGHT, (548, 418, 132, 74))

        map_title = self.font_large.render("Hoenn Routes", True, TEXT_WHITE)
        self.screen.blit(map_title, (28, 22))
        badge_text = f"Badges: {len(self.badges)}/8"
        badge_label = self.font_small.render(badge_text, True, TEXT_WHITE)
        badge_rect = badge_label.get_rect(topright=(SCREEN_WIDTH - 34, 28))
        pygame.draw.rect(self.screen, OUTLINE, badge_rect.inflate(12, 8), border_radius=5)
        self.screen.blit(badge_label, badge_rect)

        for start, end in REGION_ROUTE_LINKS:
            start_pos = REGION_NODE_POSITIONS[start]
            end_pos = REGION_NODE_POSITIONS[end]
            pygame.draw.line(self.screen, OUTLINE, start_pos, end_pos, 10)
            pygame.draw.line(self.screen, PATH, start_pos, end_pos, 6)

        for index, node_stop in enumerate(REGION_STOPS):
            self.draw_region_node(index, node_stop)

        player_x, player_y = REGION_NODE_POSITIONS[self.region_index]
        pygame.draw.circle(self.screen, TEXT_GOLD, (player_x, player_y - 24), 12)
        pygame.draw.circle(self.screen, OUTLINE, (player_x, player_y - 24), 12, 3)
        pygame.draw.polygon(
            self.screen,
            OUTLINE,
            [(player_x - 8, player_y - 14), (player_x + 8, player_y - 14), (player_x, player_y - 3)],
        )

        self.draw_region_info_panel(stop)

    def draw_region_node(self, index, stop):
        """Draw a town, route, cave, or gym marker on the region map."""
        x, y = REGION_NODE_POSITIONS[index]
        kind = stop["kind"]
        selected = index == self.region_index
        colors = {
            "town": (247, 251, 255),
            "route": (246, 224, 171),
            "forest": TREE,
            "cave": (142, 132, 124),
            "gym": (255, 221, 92),
            "league": (190, 213, 255),
        }
        radius = 13 if kind in {"town", "gym", "league"} else 9
        outline = TEXT_GOLD if selected else OUTLINE
        pygame.draw.circle(self.screen, outline, (x, y), radius + 4)
        pygame.draw.circle(self.screen, colors.get(kind, UI_PANEL), (x, y), radius)
        if kind == "gym" and stop.get("badge") in self.badges:
            pygame.draw.circle(self.screen, SAPPHIRE_DEEP, (x, y), 5)
        if selected or kind in {"town", "gym", "league"}:
            label = self.font_small.render(stop["name"], True, OUTLINE)
            label_rect = label.get_rect(center=(x, y + radius + 15))
            pygame.draw.rect(self.screen, UI_PANEL, label_rect.inflate(8, 4), border_radius=4)
            self.screen.blit(label, label_rect)

    def draw_region_info_panel(self, stop):
        title_panel = pygame.Rect(54, SCREEN_HEIGHT - 154, SCREEN_WIDTH - 108, 116)
        self.draw_gba_panel(title_panel, (255, 250, 217))
        title = self.font_medium.render(stop["name"], True, OUTLINE)
        subtitle = self.font_small.render(stop["subtitle"], True, TEXT_BLUE)
        self.screen.blit(title, (title_panel.x + 24, title_panel.y + 16))
        self.screen.blit(subtitle, (title_panel.x + 24, title_panel.y + 46))
        for index, line in enumerate(stop["lines"][:2]):
            text = self.font_small.render(line, True, OUTLINE)
            self.screen.blit(text, (title_panel.x + 24, title_panel.y + 72 + index * 20))

        if stop.get("badge") and stop["badge"] not in self.badges:
            prompt = f"ENTER: win {stop['badge']}"
        else:
            prompt = "ARROWS: travel  ENTER: visit  B: Bag  P: Pokedex  ESC: Bluebell"
        prompt_text = self.font_small.render(prompt, True, TEXT_BLUE)
        prompt_rect = prompt_text.get_rect(right=title_panel.right - 24, bottom=title_panel.bottom - 14)
        self.screen.blit(prompt_text, prompt_rect)

    def start_route_exploration(self, entry_side="south"):
        """Build and enter a walkable route map for the selected region stop."""
        self.route_map = self.build_route_map(REGION_STOPS[self.region_index])
        entry_positions = {
            "north": (10, 1, "down"),
            "south": (10, 13, "up"),
            "west": (1, 7, "right"),
            "east": (18, 7, "left"),
        }
        self.route_player_x, self.route_player_y, self.player_direction = entry_positions.get(entry_side, entry_positions["south"])
        self.state = STATE_ROUTE_EXPLORE

    def build_route_map(self, stop):
        """Create a compact route with paths, tall grass, and edge exits."""
        route_map = [[TILE_GRASS for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if x == 0 or x == MAP_WIDTH - 1 or y == 0 or y == MAP_HEIGHT - 1:
                    route_map[y][x] = TILE_TREE

        for x in range(1, MAP_WIDTH - 1):
            route_map[7][x] = TILE_PATH
        for y in range(1, MAP_HEIGHT - 1):
            route_map[y][10] = TILE_PATH

        for y in range(2, 6):
            for x in range(2, 8):
                route_map[y][x] = TILE_TALL_GRASS
        for y in range(9, 13):
            for x in range(12, 18):
                route_map[y][x] = TILE_TALL_GRASS
        if stop["kind"] == "forest":
            for y in range(2, 13):
                if y != 7:
                    route_map[y][4] = TILE_TREE
                    route_map[y][15] = TILE_TREE
        elif stop["kind"] == "cave":
            for y in range(2, 13):
                for x in range(2, 18):
                    if route_map[y][x] == TILE_GRASS:
                        route_map[y][x] = TILE_TALL_GRASS if (x + y) % 4 == 0 else TILE_PATH

        for side, opening in {"north": (10, 0), "south": (10, 14), "west": (0, 7), "east": (19, 7)}.items():
            if self.get_region_neighbor_for_side(side) is not None:
                open_x, open_y = opening
                route_map[open_y][open_x] = TILE_PATH
        return route_map

    def get_region_neighbor_for_side(self, side):
        key_for_side = {
            "north": pygame.K_UP,
            "south": pygame.K_DOWN,
            "west": pygame.K_LEFT,
            "east": pygame.K_RIGHT,
        }[side]
        return self.get_region_neighbor_for_key(key_for_side)

    def is_route_solid(self, x, y):
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return False
        return self.route_map[y][x] in SOLID_TILES

    def draw_route_explore(self):
        """Draw the walkable route with tall grass encounter zones."""
        stop = REGION_STOPS[self.region_index]
        if self.route_map is None:
            self.start_route_exploration()

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                self.draw_tile(x, y, self.route_map[y][x])

        title_panel = pygame.Rect(MAP_OFFSET_X + 10, MAP_OFFSET_Y + 10, 230, 46)
        self.draw_gba_panel(title_panel, (255, 250, 217))
        title = self.font_small.render(stop["name"], True, OUTLINE)
        self.screen.blit(title, (title_panel.x + 18, title_panel.y + 14))

        self.draw_player_at(self.route_player_x, self.route_player_y)
        self.draw_dialog_box(["Walk through tall grass to search for Pokemon.", "Reach a path exit or press ESC for the region map."], "ARROWS")

    def draw_wild_encounter(self):
        """Show the result of a tall-grass encounter."""
        self.draw_route_explore()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(80)
        overlay.fill((9, 34, 74))
        self.screen.blit(overlay, (0, 0))

        encounter_panel = pygame.Rect(210, 122, 380, 260)
        self.draw_gba_panel(encounter_panel, (255, 250, 217))
        pokemon_name = self.wild_encounter_name or "poochyena"
        self.draw_battle_pokemon(pokemon_name, (SCREEN_WIDTH // 2, 276), 130)
        title = self.font_large.render(f"Wild {pokemon_name.capitalize()}!", True, OUTLINE)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 162)))
        level = self.font_medium.render(f"Lv.{self.wild_encounter_level}", True, TEXT_BLUE)
        self.screen.blit(level, level.get_rect(center=(SCREEN_WIDTH // 2, 322)))
        self.draw_dialog_box(["A wild Pokemon jumped out of the tall grass!", "Press ENTER to battle it!"], "ENTER")

    def draw_sprite_with_shadow(self, name, midbottom):
        sprite = self.pokemon_sprites.get(name)
        if not sprite:
            return
        rect = sprite.get_rect(midbottom=midbottom)
        pygame.draw.ellipse(
            self.screen,
            (81, 120, 82),
            (rect.x + 4, rect.bottom - 8, max(12, rect.width - 8), 8),
        )
        self.screen.blit(sprite, rect)

    def draw_hp_bar(self, x, y, label, level, hp, max_hp):
        panel = pygame.Rect(x, y, 190, 54)
        self.draw_gba_panel(panel)
        name_text = self.font_small.render(label, True, OUTLINE)
        self.screen.blit(name_text, (panel.x + 12, panel.y + 8))
        level_text = self.font_small.render(f"Lv.{level}", True, OUTLINE)
        level_rect = level_text.get_rect(topright=(panel.right - 12, panel.y + 8))
        self.screen.blit(level_text, level_rect)
        pygame.draw.rect(self.screen, OUTLINE, (panel.x + 12, panel.y + 32, 142, 10), border_radius=4)
        fill_width = max(0, int(138 * hp / max_hp))
        hp_color = (74, 190, 98) if hp > max_hp // 2 else (242, 178, 66)
        pygame.draw.rect(self.screen, hp_color, (panel.x + 14, panel.y + 34, fill_width, 6), border_radius=3)

    def draw_battle_platform(self, center, size, top_color, side_color):
        x, y = center
        width, height = size
        shadow = pygame.Rect(0, 0, width + 36, height + 18)
        shadow.center = (x, y + 18)
        pygame.draw.ellipse(self.screen, (67, 116, 93), shadow)
        side = pygame.Rect(0, 0, width, height)
        side.center = (x, y + 12)
        pygame.draw.ellipse(self.screen, side_color, side)
        top = pygame.Rect(0, 0, width, height)
        top.center = center
        pygame.draw.ellipse(self.screen, OUTLINE, top.inflate(8, 8))
        pygame.draw.ellipse(self.screen, top_color, top)
        pygame.draw.arc(self.screen, (255, 247, 194), top.inflate(-20, -10), 3.35, 5.95, 3)

    def draw_battle_pokemon(self, name, midbottom, max_size):
        sprite = self.pokemon_sprites.get(name)
        if not sprite:
            return
        width, height = sprite.get_size()
        scale = min(max_size / width, max_size / height)
        battle_sprite = pygame.transform.scale(sprite, (int(width * scale), int(height * scale)))
        rect = battle_sprite.get_rect(midbottom=midbottom)
        pygame.draw.ellipse(
            self.screen,
            (57, 93, 76),
            (rect.x + 8, rect.bottom - 12, max(22, rect.width - 16), 14),
        )
        self.screen.blit(battle_sprite, rect)

    def add_floating_text(self, text, pos, color):
        """Create a short-lived battle text popup that floats upward."""
        self.floating_texts.append({
            "text": text,
            "x": pos[0],
            "y": pos[1],
            "color": color,
            "timer": 45,
        })

    def update_floating_texts(self):
        active = []
        for item in self.floating_texts:
            item["y"] -= 0.7
            item["timer"] -= 1
            if item["timer"] > 0:
                active.append(item)
        self.floating_texts = active

    def draw_floating_texts(self):
        for item in self.floating_texts:
            text = self.font_small.render(item["text"], True, item["color"])
            rect = text.get_rect(center=(int(item["x"]), int(item["y"])))
            self.screen.blit(text, rect)

    def ensure_starter_in_party(self):
        if not self.starter_name:
            return
        if self.starter_name not in self.party_pokemon:
            self.party_pokemon.insert(0, self.starter_name)
        if self.active_party_index >= len(self.party_pokemon):
            self.active_party_index = 0

    def get_active_battle_pokemon_name(self):
        self.ensure_starter_in_party()
        if not self.party_pokemon:
            return self.starter_name or "treecko"
        return self.party_pokemon[self.active_party_index]

    def get_active_battle_level(self):
        return max(2, self.starter_level - 1) if self.get_active_battle_pokemon_name() != self.starter_name else self.starter_level

    def get_active_battle_moves(self):
        name = self.get_active_battle_pokemon_name()
        if name in STARTER_MOVES:
            return STARTER_MOVES[name]
        return [
            {"name": "Tackle", "power": 5, "accuracy": 95},
            {"name": "Quick Attack", "power": 5, "accuracy": 100},
            {"name": "Bite", "power": 6, "accuracy": 92},
            {"name": "Growl", "power": 3, "accuracy": 100},
        ]

    def draw_battle_scene(self):
        """Draw a separate, more dimensional Pokemon-style battle screen."""
        active_name = self.get_active_battle_pokemon_name()
        starter = active_name.capitalize()
        wild_name = self.active_wild_name.capitalize()
        wild_level = self.active_wild_level
        self.update_floating_texts()

        self.screen.fill(SAPPHIRE_LIGHT)
        pygame.draw.rect(self.screen, (226, 247, 255), (0, 0, SCREEN_WIDTH, 92))
        pygame.draw.rect(self.screen, SAPPHIRE_LIGHT, (0, 92, SCREEN_WIDTH, 72))
        pygame.draw.rect(self.screen, (132, 212, 145), (0, 164, SCREEN_WIDTH, 246))
        for stripe_y in range(176, 390, 28):
            pygame.draw.line(self.screen, (112, 196, 132), (0, stripe_y), (SCREEN_WIDTH, stripe_y - 42), 2)
        pygame.draw.polygon(
            self.screen,
            (91, 185, 119),
            [(0, 410), (SCREEN_WIDTH, 410), (620, 250), (180, 250)],
        )
        pygame.draw.polygon(
            self.screen,
            (236, 211, 139),
            [(196, 410), (604, 410), (488, 272), (314, 272)],
        )
        for offset in range(0, SCREEN_WIDTH, 92):
            pygame.draw.circle(self.screen, TREE_DARK, (offset + 34, 140), 34)
            pygame.draw.circle(self.screen, TREE, (offset + 48, 128), 26)

        self.draw_battle_platform((560, 236), (210, 70), (121, 214, 126), (70, 159, 98))
        self.draw_battle_platform((238, 358), (260, 88), (121, 214, 126), (70, 159, 98))
        self.draw_battle_pokemon(self.active_wild_name, (560, 224), 86)
        if self.battle_intro_timer <= 0:
            self.draw_battle_pokemon(active_name, (238, 342), 122)
        self.draw_hp_bar(72, 104, starter, self.get_active_battle_level(), self.player_battle_hp, self.player_max_hp)
        self.draw_hp_bar(526, 86, wild_name, wild_level, self.wild_battle_hp, self.wild_max_hp)

        if self.battle_intro_timer > 0:
            self.draw_battle_intro_animation(starter)
            self.battle_intro_timer -= 1
        if self.attack_anim_timer > 0:
            self.draw_attack_animation()
            self.attack_anim_timer -= 1

        command_box = pygame.Rect(48, 410, SCREEN_WIDTH - 96, 138)
        self.draw_gba_panel(command_box)

        if self.battle_intro_timer > 0:
            intro_text = self.font_medium.render(f"{starter}, I choose you!", True, OUTLINE)
            self.screen.blit(intro_text, (command_box.x + 24, command_box.y + 34))
        elif self.event_step == 3:
            if self.battle_submenu == "main":
                prompt = self.font_medium.render(f"What will {starter} do?", True, OUTLINE)
                self.screen.blit(prompt, (command_box.x + 24, command_box.y + 18))
                actions = ["Fight", "Bag", "Run", "Pokemon"]
                for index, action in enumerate(actions):
                    col = index % 2
                    row = index // 2
                    action_rect = pygame.Rect(command_box.x + 300 + col * 170, command_box.y + 14 + row * 50, 150, 40)
                    selected = index == self.selected_battle_action
                    color = (255, 248, 207) if selected else (233, 244, 255)
                    outline = TEXT_GOLD if selected else OUTLINE
                    self.draw_rounded_rect(action_rect, color, radius=7, outline_color=outline, outline_width=2)
                    label = self.font_medium.render(action, True, OUTLINE)
                    self.screen.blit(label, (action_rect.x + 12, action_rect.y + 6))
            elif self.battle_submenu == "fight":
                prompt = self.font_medium.render(f"Choose a move for {starter}:", True, OUTLINE)
                self.screen.blit(prompt, (command_box.x + 24, command_box.y + 18))
                moves = self.get_active_battle_moves()
                for index, move in enumerate(moves):
                    col = index % 2
                    row = index // 2
                    move_rect = pygame.Rect(command_box.x + 300 + col * 170, command_box.y + 14 + row * 50, 150, 40)
                    selected = index == self.selected_move
                    color = (255, 248, 207) if selected else (233, 244, 255)
                    outline = TEXT_GOLD if selected else OUTLINE
                    self.draw_rounded_rect(move_rect, color, radius=7, outline_color=outline, outline_width=2)
                    move_text = self.font_small.render(move["name"], True, OUTLINE)
                    self.screen.blit(move_text, (move_rect.x + 10, move_rect.y + 4))
                    dmg_text = self.font_small.render(f"DMG {move['power']}", True, TEXT_BLUE)
                    dmg_rect = dmg_text.get_rect(right=move_rect.right - 10, bottom=move_rect.bottom - 3)
                    self.screen.blit(dmg_text, dmg_rect)
            elif self.battle_submenu == "bag":
                items = ["Potion", "Poke Ball"]
                bag_title = self.font_medium.render("Bag", True, OUTLINE)
                self.screen.blit(bag_title, (command_box.x + 24, command_box.y + 18))
                for idx, item in enumerate(items):
                    row_rect = pygame.Rect(command_box.x + 200, command_box.y + 16 + idx * 48, 260, 40)
                    selected = idx == self.battle_bag_selection
                    color = (255, 248, 207) if selected else (233, 244, 255)
                    outline = TEXT_GOLD if selected else OUTLINE
                    self.draw_rounded_rect(row_rect, color, radius=7, outline_color=outline, outline_width=2)
                    text = self.font_small.render(f"{item} x{self.bag_items.get(item, 0)}", True, OUTLINE)
                    self.screen.blit(text, (row_rect.x + 12, row_rect.y + 9))
                hint = self.font_small.render("ENTER use  ESC back", True, TEXT_BLUE)
                self.screen.blit(hint, (command_box.x + 24, command_box.bottom - 28))
            elif self.battle_submenu == "pokemon":
                party_title = self.font_medium.render("Choose Pokemon", True, OUTLINE)
                self.screen.blit(party_title, (command_box.x + 24, command_box.y + 18))
                for idx, name in enumerate(self.party_pokemon[:4]):
                    row_rect = pygame.Rect(command_box.x + 200, command_box.y + 10 + idx * 31, 260, 28)
                    selected = idx == self.battle_party_selection
                    color = (255, 248, 207) if selected else (233, 244, 255)
                    outline = TEXT_GOLD if selected else OUTLINE
                    self.draw_rounded_rect(row_rect, color, radius=6, outline_color=outline, outline_width=2)
                    text = self.font_small.render(name.capitalize(), True, OUTLINE)
                    self.screen.blit(text, (row_rect.x + 10, row_rect.y + 5))
                hint = self.font_small.render("ENTER switch  ESC back", True, TEXT_BLUE)
                self.screen.blit(hint, (command_box.x + 24, command_box.bottom - 28))
        else:
            lines = self.battle_message.split("\n")
            for index, line in enumerate(lines):
                text = self.font_medium.render(line, True, OUTLINE)
                self.screen.blit(text, (command_box.x + 24, command_box.y + 24 + index * 32))
            prompt = self.font_small.render("Press ENTER", True, TEXT_BLUE)
            prompt_rect = prompt.get_rect(right=command_box.right - 24, bottom=command_box.bottom - 16)
            self.screen.blit(prompt, prompt_rect)
        self.draw_floating_texts()

    def draw_battle_intro_animation(self, starter):
        """Animate trainer throw, ball open, and Pokemon send-out."""
        progress = (self.battle_intro_total - self.battle_intro_timer) / max(1, self.battle_intro_total)
        progress = max(0.0, min(1.0, progress))

        trainer_x = int(80 + 36 * min(1.0, progress * 1.2))
        trainer_y = 328
        pygame.draw.circle(self.screen, (239, 214, 191), (trainer_x + 18, trainer_y - 24), 12)
        pygame.draw.rect(self.screen, PLAYER_COLOR, (trainer_x + 8, trainer_y - 10, 20, 32), border_radius=5)
        pygame.draw.rect(self.screen, (59, 74, 104), (trainer_x + 4, trainer_y + 18, 10, 16), border_radius=3)
        pygame.draw.rect(self.screen, (59, 74, 104), (trainer_x + 22, trainer_y + 18, 10, 16), border_radius=3)

        ball_origin = (trainer_x + 28, 300)
        ball_target = (238, 316)
        throw_end = 0.56
        open_end = 0.76

        if progress <= throw_end:
            t = progress / throw_end
            ball_x = int(ball_origin[0] + (ball_target[0] - ball_origin[0]) * t)
            parabola = 4 * t * (1 - t)
            ball_y = int(ball_origin[1] + (ball_target[1] - ball_origin[1]) * t - 110 * parabola)
            self.draw_pokeball_sprite(ball_x, ball_y, 8, seam_angle=18 * (1 - t))
        elif progress <= open_end:
            t = (progress - throw_end) / max(0.001, (open_end - throw_end))
            ball_x, ball_y = ball_target
            lid_offset = int(12 * t)
            pygame.draw.circle(self.screen, OUTLINE, (ball_x, ball_y), 9, 2)
            pygame.draw.circle(self.screen, (248, 248, 248), (ball_x, ball_y + 3), 8)
            pygame.draw.circle(self.screen, (242, 66, 66), (ball_x, ball_y - 3 - lid_offset), 8)
            for r in (16, 26, 36):
                pygame.draw.circle(self.screen, (255, 245, 190), (ball_x, ball_y - 2), int(r * t), 2)
        else:
            t = (progress - open_end) / max(0.001, (1.0 - open_end))
            pulse = 1.0 + 0.5 * t
            ring = pygame.Rect(0, 0, int(92 * pulse), int(38 * pulse))
            ring.center = (238, 340)
            pygame.draw.ellipse(self.screen, (252, 246, 179), ring, 3)
            glow_radius = int(24 + 40 * t)
            pygame.draw.circle(self.screen, (255, 245, 210), (238, 328), glow_radius, 2)

    def draw_pokeball_sprite(self, x, y, radius, seam_angle=0):
        pygame.draw.circle(self.screen, OUTLINE, (x, y), radius + 1)
        pygame.draw.circle(self.screen, (242, 66, 66), (x, y - 1), radius)
        pygame.draw.circle(self.screen, (248, 248, 248), (x, y + 2), radius - 1)
        pygame.draw.line(self.screen, OUTLINE, (x - radius, y), (x + radius, y), 2)
        seam_dx = int(radius * 0.7 * (seam_angle / 18.0))
        pygame.draw.circle(self.screen, OUTLINE, (x + seam_dx, y), 3, 2)
        pygame.draw.circle(self.screen, (240, 240, 240), (x + seam_dx, y), 2)

    def start_attack_animation(self, move_name, target="wild", from_side="player"):
        self.attack_anim_move = move_name.lower()
        self.attack_anim_target = target
        self.attack_anim_from = from_side
        self.attack_anim_total = 28
        self.attack_anim_timer = self.attack_anim_total

    def draw_attack_animation(self):
        if self.attack_anim_timer <= 0:
            return
        progress = 1.0 - self.attack_anim_timer / max(1, self.attack_anim_total)
        target_pos = (560, 224) if self.attack_anim_target == "wild" else (238, 342)
        source_pos = (238, 342) if self.attack_anim_from == "player" else (560, 224)
        move = self.attack_anim_move

        if "ember" in move or "fire" in move:
            for i in range(5):
                t = max(0.0, min(1.0, progress - i * 0.08))
                x = int(source_pos[0] + (target_pos[0] - source_pos[0]) * t)
                y = int(source_pos[1] + (target_pos[1] - source_pos[1]) * t - 22 * (1 - t) * t)
                pygame.draw.circle(self.screen, (255, 130, 52), (x, y), 6)
                pygame.draw.circle(self.screen, (255, 213, 120), (x, y), 3)
        elif "water" in move:
            for i in range(6):
                t = max(0.0, min(1.0, progress - i * 0.05))
                x = int(source_pos[0] + (target_pos[0] - source_pos[0]) * t)
                y = int(source_pos[1] + (target_pos[1] - source_pos[1]) * t + 12 * ((i % 2) * 2 - 1))
                pygame.draw.circle(self.screen, (105, 208, 252), (x, y), 4)
        elif "absorb" in move:
            for i in range(5):
                t = max(0.0, min(1.0, progress - i * 0.06))
                x = int(target_pos[0] + (source_pos[0] - target_pos[0]) * t)
                y = int(target_pos[1] + (source_pos[1] - target_pos[1]) * t)
                pygame.draw.circle(self.screen, (96, 224, 124), (x, y), 5)
        elif "quick" in move:
            dash_t = min(1.0, progress * 1.6)
            x = int(source_pos[0] + (target_pos[0] - source_pos[0]) * dash_t)
            y = int(source_pos[1] + (target_pos[1] - source_pos[1]) * dash_t)
            pygame.draw.line(self.screen, (255, 255, 255), source_pos, (x, y), 5)
            pygame.draw.line(self.screen, (187, 236, 255), source_pos, (x, y), 2)
        elif "scratch" in move or "slash" in move or "bite" in move:
            for i in range(3):
                offset = i * 10 - 10
                slash = pygame.Rect(0, 0, 54, 12)
                slash.center = (target_pos[0] + offset, target_pos[1] - 18 + offset // 2)
                pygame.draw.line(self.screen, (255, 244, 186), slash.topleft, slash.bottomright, 3)
                pygame.draw.line(self.screen, (255, 255, 255), (slash.x + 8, slash.y), (slash.right, slash.bottom - 8), 2)
        elif "growl" in move or "leer" in move:
            for i in range(3):
                radius = int(18 + progress * 52 + i * 12)
                pygame.draw.circle(self.screen, (255, 241, 178), source_pos, radius, 2)
        elif "mud" in move:
            for i in range(6):
                t = max(0.0, min(1.0, progress - i * 0.05))
                x = int(source_pos[0] + (target_pos[0] - source_pos[0]) * t)
                y = int(source_pos[1] + (target_pos[1] - source_pos[1]) * t + 20 * (1 - t))
                pygame.draw.circle(self.screen, (153, 111, 70), (x, y), 4)
        else:
            impact = int(10 + 18 * (1 - abs(progress - 0.55) * 2))
            pygame.draw.circle(self.screen, (255, 245, 190), target_pos, max(6, impact), 2)

    def start_wild_battle(self):
        """Enter a mandatory wild battle after an encounter."""
        self.ensure_starter_in_party()
        self.active_wild_name = self.wild_encounter_name or "poochyena"
        self.active_wild_level = self.wild_encounter_level
        self.discover_pokemon(self.active_wild_name)
        self.in_wild_battle = True
        self.player_battle_hp = self.player_max_hp
        self.wild_max_hp = 10 + self.active_wild_level * 2
        self.wild_battle_hp = self.wild_max_hp
        self.selected_move = 0
        self.floating_texts = []
        self.event_step = 3
        self.battle_intro_timer = self.battle_intro_total
        self.battle_submenu = "main"
        self.selected_battle_action = 0
        self.battle_message = f"A wild {self.active_wild_name.capitalize()} appeared!"
        self.state = STATE_BATTLE

    def draw_route_event(self):
        """Draw the rescue sequence on the northern route."""
        self.screen.fill((122, 203, 151))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                color = GRASS if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0 else GRASS_LIGHT
                pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(self.screen, PATH, (0, 250, SCREEN_WIDTH, 74), border_radius=18)
        for x in range(40, SCREEN_WIDTH, 86):
            pygame.draw.circle(self.screen, TREE_DARK, (x, 88), 24)
            pygame.draw.circle(self.screen, TREE, (x + 8, 82), 18)

        professor_x = 350 if self.event_step < 4 else 230
        professor_y = 226 if self.event_step < 4 else 238
        pygame.draw.circle(self.screen, (239, 214, 191), (professor_x + 16, professor_y - 16), 17)
        pygame.draw.rect(self.screen, (94, 171, 230), (professor_x, professor_y, 32, 46), border_radius=8)
        professor_label = self.font_small.render("PROF.", True, OUTLINE)
        self.screen.blit(professor_label, (professor_x - 4, professor_y + 52))

        self.draw_sprite_with_shadow("poochyena", (494, 304))
        wild_label = self.font_small.render("Wild Poochyena", True, OUTLINE)
        wild_level = self.starter_level + 1
        self.screen.blit(wild_label, (430, 306))
        wild_level_label = self.font_small.render(f"Lv.{wild_level}", True, OUTLINE)
        self.screen.blit(wild_level_label, (430, 326))

        if self.event_step == 0:
            self.discover_pokemon("poochyena")
            self.draw_dialog_box(["Professor Birch: Help! A wild Pokemon", "is attacking me on the north trail!"])
        elif self.event_step == 1:
            self.draw_starter_selection()
        elif self.event_step == 2:
            starter = self.starter_name.capitalize()
            sprite = self.pokemon_sprites.get(self.starter_name)
            if sprite:
                rect = sprite.get_rect(midbottom=(318, 304))
                self.screen.blit(sprite, rect)
            self.draw_dialog_box([f"{starter} Lv.{self.starter_level}, I choose you!", f"{starter} drove the wild Pokemon away!"])
        else:
            starter = self.starter_name.capitalize()
            self.draw_dialog_box(["Professor Birch: Thank you!", f"Keep {starter}. Your journey begins now."], "ENTER")

    def draw_starter_selection(self):
        title = self.font_medium.render("Choose a starter for the northern route:", True, OUTLINE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 316))
        self.screen.blit(title, title_rect)
        for index, name in enumerate(STARTER_NAMES):
            card = pygame.Rect(206 + index * 132, 340, 112, 92)
            selected = index == self.starter_choice
            card_color = (255, 248, 207) if selected else UI_PANEL
            outline = TEXT_GOLD if selected else OUTLINE
            self.draw_rounded_rect(card, card_color, radius=10, outline_color=outline, outline_width=4)
            sprite = self.pokemon_sprites.get(name)
            if sprite:
                rect = sprite.get_rect(center=(card.centerx, card.y + 40))
                self.screen.blit(sprite, rect)
            label = self.font_small.render(name.capitalize(), True, OUTLINE)
            label_rect = label.get_rect(center=(card.centerx, card.y + 72))
            self.screen.blit(label, label_rect)
        self.draw_dialog_box(["Use LEFT / RIGHT, then ENTER.", "Then head north to assist the professor."], "ENTER")
    
    def handle_title_input(self, event):
        """Handle input on title screen"""
        if event.key == pygame.K_RETURN:
            self.state = STATE_NAME_ENTRY
        elif event.key == pygame.K_t:
            self.state = STATE_TEST_REGION_PICKER

    def handle_test_region_picker_input(self, event):
        """Handle the developer start-region picker."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_TITLE
        elif event.key == pygame.K_UP:
            self.test_region_index = max(0, self.test_region_index - 1)
        elif event.key == pygame.K_DOWN:
            self.test_region_index = min(len(REGION_STOPS) - 1, self.test_region_index + 1)
        elif event.key == pygame.K_PAGEUP:
            self.test_region_index = max(0, self.test_region_index - 10)
        elif event.key == pygame.K_PAGEDOWN:
            self.test_region_index = min(len(REGION_STOPS) - 1, self.test_region_index + 10)
        elif event.key == pygame.K_HOME:
            self.test_region_index = 0
        elif event.key == pygame.K_END:
            self.test_region_index = len(REGION_STOPS) - 1
        elif event.key == pygame.K_RETURN:
            self.start_test_run(self.test_region_index)

    def start_test_run(self, region_index):
        """Skip story setup and begin testing at a chosen region stop."""
        self.player_name = "TESTER"
        self.starter_name = self.starter_name or STARTER_NAMES[self.starter_choice]
        self.ensure_starter_in_party()
        self.starter_level = max(self.starter_level, 12)
        self.player_max_hp = 28
        self.player_battle_hp = self.player_max_hp
        self.professor_rescued = True
        self.trail_unlocked = True
        self.region_index = region_index
        self.route_map = None
        self.floating_texts = []
        stop = REGION_STOPS[self.region_index]
        if stop["kind"] in {"route", "forest", "cave"}:
            self.start_route_exploration()
        else:
            self.state = STATE_NEXT_TOWN
    
    def handle_name_entry_input(self, event):
        """Handle input on name entry screen"""
        if event.key == pygame.K_RETURN:
            if len(self.player_name) > 0:
                self.state = STATE_TOWN
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif len(self.player_name) < 12:
            # Allow alphanumeric and spaces
            if event.unicode.isalnum() or event.unicode == ' ':
                self.player_name += event.unicode
    
    def handle_town_input(self, event):
        """Handle input in town"""
        building = self.get_building_at_player()
        if event.key == pygame.K_RETURN and building:
            self.current_building = building
            self.try_find_stone("building", building["id"])
            self.state = STATE_BUILDING
            return

        if event.key == pygame.K_RETURN and self.player_at_route_assist():
            if not self.professor_rescued:
                self.state = STATE_ROUTE_EVENT
                self.event_step = 0
                self.player_battle_hp = self.player_max_hp
                self.wild_battle_hp = self.wild_max_hp
                self.selected_move = 0
                self.battle_message = ""
            elif self.trail_unlocked:
                self.state = STATE_NEXT_TOWN
            return

        new_x, new_y = self.player_x, self.player_y
        
        if event.key == pygame.K_UP:
            new_y -= 1
            self.player_direction = "up"
        elif event.key == pygame.K_DOWN:
            new_y += 1
            self.player_direction = "down"
        elif event.key == pygame.K_LEFT:
            new_x -= 1
            self.player_direction = "left"
        elif event.key == pygame.K_RIGHT:
            new_x += 1
            self.player_direction = "right"
        
        # Check if the new position is valid
        if not self.is_solid(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
        
        # Update animation
        self.player_anim_timer += 1
        if self.player_anim_timer > 8:
            self.player_anim_timer = 0
            self.player_anim_frame = (self.player_anim_frame + 1) % 3

    def handle_building_input(self, event):
        """Handle homes and lab interactions."""
        if event.key == pygame.K_ESCAPE:
            if self.current_building and self.current_building["kind"] == "lab" and self.professor_rescued:
                self.trail_unlocked = True
            self.state = STATE_TOWN
            self.current_building = None
            return

        if self.current_building and self.current_building["kind"] == "lab" and not self.starter_name:
            if event.key == pygame.K_LEFT:
                self.starter_choice = (self.starter_choice - 1) % len(STARTER_NAMES)
            elif event.key == pygame.K_RIGHT:
                self.starter_choice = (self.starter_choice + 1) % len(STARTER_NAMES)
            elif event.key == pygame.K_RETURN:
                self.starter_name = STARTER_NAMES[self.starter_choice]
                self.starter_level = 5
                self.discover_pokemon(self.starter_name)
                self.ensure_starter_in_party()
        elif event.key == pygame.K_RETURN:
            if self.current_building and self.current_building["kind"] == "lab" and self.professor_rescued:
                self.trail_unlocked = True
            self.state = STATE_TOWN
            self.current_building = None

    def handle_next_town_input(self, event):
        """Move around the open region map or visit the selected stop."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_TOWN
            self.player_x, self.player_y = ROUTE_ASSIST_TILE
            self.player_direction = "down"
            return

        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            next_index = self.get_region_neighbor_for_key(event.key)
            if next_index is not None:
                self.region_index = next_index
            return

        if event.key == pygame.K_RETURN:
            stop = REGION_STOPS[self.region_index]
            self.try_find_stone("region", stop["name"])
            if stop["kind"] in {"route", "forest", "cave"}:
                self.start_route_exploration()
                return
            badge = stop.get("badge")
            if badge and badge not in self.badges:
                self.badges.append(badge)
                self.handle_starter_level_up()

    def get_region_neighbor_for_key(self, key):
        """Pick the connected region stop that best matches the pressed direction."""
        current_x, current_y = REGION_NODE_POSITIONS[self.region_index]
        options = []
        for neighbor in REGION_LINK_LOOKUP[self.region_index]:
            neighbor_x, neighbor_y = REGION_NODE_POSITIONS[neighbor]
            dx = neighbor_x - current_x
            dy = neighbor_y - current_y
            if key == pygame.K_UP and dy < 0:
                options.append((abs(dx) + abs(dy), abs(dx), neighbor))
            elif key == pygame.K_DOWN and dy > 0:
                options.append((abs(dx) + abs(dy), abs(dx), neighbor))
            elif key == pygame.K_LEFT and dx < 0:
                options.append((abs(dx) + abs(dy), abs(dy), neighbor))
            elif key == pygame.K_RIGHT and dx > 0:
                options.append((abs(dx) + abs(dy), abs(dy), neighbor))
        if not options:
            return None
        options.sort()
        return options[0][2]

    def handle_route_explore_input(self, event):
        """Move through a local route and roll encounters in tall grass."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_NEXT_TOWN
            return

        new_x, new_y = self.route_player_x, self.route_player_y
        side = None
        if event.key == pygame.K_UP:
            new_y -= 1
            self.player_direction = "up"
            side = "north"
        elif event.key == pygame.K_DOWN:
            new_y += 1
            self.player_direction = "down"
            side = "south"
        elif event.key == pygame.K_LEFT:
            new_x -= 1
            self.player_direction = "left"
            side = "west"
        elif event.key == pygame.K_RIGHT:
            new_x += 1
            self.player_direction = "right"
            side = "east"
        else:
            return

        if new_x < 0 or new_x >= MAP_WIDTH or new_y < 0 or new_y >= MAP_HEIGHT:
            neighbor = self.get_region_neighbor_for_side(side)
            if neighbor is not None:
                self.enter_region_neighbor(neighbor, side)
            return

        if not self.is_route_solid(new_x, new_y):
            self.route_player_x = new_x
            self.route_player_y = new_y
            self.update_player_walk_animation()
            if self.route_map[new_y][new_x] == TILE_TALL_GRASS:
                self.try_wild_encounter()

    def enter_region_neighbor(self, neighbor, exit_side):
        """Move from a route edge to the connected map node."""
        self.region_index = neighbor
        stop = REGION_STOPS[self.region_index]
        opposite_side = {
            "north": "south",
            "south": "north",
            "west": "east",
            "east": "west",
        }[exit_side]
        if stop["kind"] in {"route", "forest", "cave"}:
            self.start_route_exploration(opposite_side)
        else:
            self.route_map = None
            self.state = STATE_NEXT_TOWN

    def update_player_walk_animation(self):
        self.player_anim_timer += 1
        if self.player_anim_timer > 8:
            self.player_anim_timer = 0
            self.player_anim_frame = (self.player_anim_frame + 1) % 3

    def try_wild_encounter(self):
        """Tall grass has a chance to reveal a wild Pokemon after each step."""
        if random.random() >= 0.22:
            return
        stop = REGION_STOPS[self.region_index]
        encounter_tables = {
            "forest": ["wurmple", "shroomish", "zigzagoon", "taillow"],
            "cave": ["zubat", "geodude", "makuhita"],
            "route": ["poochyena", "zigzagoon", "wurmple", "taillow", "wingull"],
        }
        choices = encounter_tables.get(stop["kind"], WILD_POKEMON)
        self.wild_encounter_name = random.choice(choices)
        self.wild_encounter_level = random.randint(max(2, self.starter_level - 2), self.starter_level + 2)
        self.previous_state = STATE_ROUTE_EXPLORE
        self.state = STATE_WILD_ENCOUNTER

    def handle_wild_encounter_input(self, event):
        if event.key == pygame.K_RETURN:
            self.start_wild_battle()

    def handle_route_event_input(self, event):
        """Advance the northern route rescue event."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_TOWN
            return

        if self.event_step == 1:
            if event.key == pygame.K_LEFT:
                self.starter_choice = (self.starter_choice - 1) % len(STARTER_NAMES)
            elif event.key == pygame.K_RIGHT:
                self.starter_choice = (self.starter_choice + 1) % len(STARTER_NAMES)
            elif event.key == pygame.K_RETURN:
                self.starter_name = STARTER_NAMES[self.starter_choice]
                self.discover_pokemon(self.starter_name)
                self.ensure_starter_in_party()
                self.event_step = 2
            return

        if event.key == pygame.K_RETURN:
            if self.event_step == 0:
                self.event_step = 1
            elif self.event_step == 2:
                self.event_step = 3
                self.active_wild_name = "poochyena"
                self.active_wild_level = self.starter_level + 1
                self.in_wild_battle = False
                self.battle_intro_timer = self.battle_intro_total
                self.battle_submenu = "main"
                self.selected_battle_action = 0
                self.state = STATE_BATTLE
            else:
                self.handle_starter_level_up()
                self.professor_rescued = True
                self.current_building = next(building for building in BUILDINGS if building["id"] == "lab")
                self.state = STATE_BUILDING
                self.player_x, self.player_y = self.current_building["door"]
                self.player_direction = "down"

    def handle_battle_input(self, event):
        """Handle the separate move-selection battle screen."""
        if self.battle_intro_timer > 0 or self.attack_anim_timer > 0:
            return
        if self.event_step == 3:
            if self.battle_submenu == "main":
                if event.key == pygame.K_LEFT:
                    self.selected_battle_action = self.selected_battle_action - 1 if self.selected_battle_action % 2 == 1 else self.selected_battle_action + 1
                elif event.key == pygame.K_RIGHT:
                    self.selected_battle_action = self.selected_battle_action + 1 if self.selected_battle_action % 2 == 0 else self.selected_battle_action - 1
                elif event.key == pygame.K_UP:
                    self.selected_battle_action = (self.selected_battle_action - 2) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected_battle_action = (self.selected_battle_action + 2) % 4
                elif event.key == pygame.K_RETURN:
                    if self.selected_battle_action == 0:
                        self.battle_submenu = "fight"
                    elif self.selected_battle_action == 1:
                        self.battle_submenu = "bag"
                    elif self.selected_battle_action == 2:
                        if self.in_wild_battle:
                            self.battle_message = "You ran away safely!"
                            self.event_step = 6
                        else:
                            self.battle_message = "You can't run from this battle!"
                            self.event_step = 5
                    elif self.selected_battle_action == 3:
                        self.battle_submenu = "pokemon"
                        self.battle_party_selection = self.active_party_index
            elif self.battle_submenu == "fight":
                if event.key == pygame.K_LEFT:
                    self.selected_move = self.selected_move - 1 if self.selected_move % 2 == 1 else self.selected_move + 1
                elif event.key == pygame.K_RIGHT:
                    self.selected_move = self.selected_move + 1 if self.selected_move % 2 == 0 else self.selected_move - 1
                elif event.key == pygame.K_UP:
                    self.selected_move = (self.selected_move - 2) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected_move = (self.selected_move + 2) % 4
                elif event.key == pygame.K_ESCAPE:
                    self.battle_submenu = "main"
                elif event.key == pygame.K_RETURN:
                    self.use_selected_move()
            elif self.battle_submenu == "bag":
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.battle_bag_selection = 1 - self.battle_bag_selection
                elif event.key == pygame.K_ESCAPE:
                    self.battle_submenu = "main"
                elif event.key == pygame.K_RETURN:
                    self.use_selected_battle_bag_item()
            elif self.battle_submenu == "pokemon":
                if event.key == pygame.K_UP:
                    self.battle_party_selection = max(0, self.battle_party_selection - 1)
                elif event.key == pygame.K_DOWN:
                    max_index = min(3, max(0, len(self.party_pokemon) - 1))
                    self.battle_party_selection = min(max_index, self.battle_party_selection + 1)
                elif event.key == pygame.K_ESCAPE:
                    self.battle_submenu = "main"
                elif event.key == pygame.K_RETURN:
                    self.switch_battle_pokemon()
            return

        if event.key == pygame.K_RETURN:
            if self.event_step == 4:
                if self.wild_battle_hp <= 0:
                    self.event_step = 6
                else:
                    self.wild_pokemon_turn()
            elif self.event_step == 5:
                self.event_step = 3
                self.battle_submenu = "main"
            elif self.event_step == 6:
                if self.in_wild_battle:
                    self.in_wild_battle = False
                    self.state = STATE_ROUTE_EXPLORE
                else:
                    self.event_step = 7
                    self.state = STATE_ROUTE_EVENT
                self.battle_submenu = "main"

    def use_selected_move(self):
        """Apply the chosen starter move during battle."""
        move = self.get_active_battle_moves()[self.selected_move]
        starter = self.get_active_battle_pokemon_name().capitalize()
        wild_name = self.active_wild_name.capitalize()
        self.start_attack_animation(move["name"], target="wild", from_side="player")

        accuracy = move.get("accuracy", 100)
        if random.randint(1, 100) > accuracy:
            self.battle_message = f"{starter} used {move['name']}!\nBut it missed!"
            self.event_step = 4
            return

        wild_hp_before = self.wild_battle_hp
        self.wild_battle_hp = max(0, self.wild_battle_hp - move["power"])
        damage_dealt = wild_hp_before - self.wild_battle_hp
        if damage_dealt > 0:
            self.add_floating_text(f"-{damage_dealt} HP", (560, 170), (212, 52, 52))

        drain_ratio = move.get("drain", 0)
        drained_hp = 0
        if drain_ratio > 0 and damage_dealt > 0:
            drained_hp = max(1, int(damage_dealt * drain_ratio))
            self.player_battle_hp = min(self.player_max_hp, self.player_battle_hp + drained_hp)
            self.add_floating_text(f"+{drained_hp} HP", (238, 294), (46, 154, 80))

        if self.wild_battle_hp == 0:
            if drained_hp > 0:
                self.battle_message = (
                    f"{starter} used {move['name']}!\n"
                    f"{starter} drained {drained_hp} HP! Wild {wild_name} fainted!"
                )
            else:
                self.battle_message = f"{starter} used {move['name']}!\nWild {wild_name} fainted!"
            self.event_step = 6
        else:
            if drained_hp > 0:
                self.battle_message = (
                    f"{starter} used {move['name']}!\n"
                    f"Wild {wild_name} took damage! {starter} drained {drained_hp} HP!"
                )
            else:
                self.battle_message = f"{starter} used {move['name']}!\nWild {wild_name} took damage!"
            self.event_step = 4
        self.battle_submenu = "main"

    def wild_pokemon_turn(self):
        """Apply the wild Pokemon's response after the player attacks."""
        wild_name = self.active_wild_name.capitalize()
        wild_move_name = "Tackle"
        wild_move_power = 4
        wild_move_accuracy = 90
        self.start_attack_animation(wild_move_name, target="player", from_side="wild")
        if random.randint(1, 100) > wild_move_accuracy:
            self.battle_message = f"Wild {wild_name} used {wild_move_name}!\nBut it missed! Choose your next move."
            self.event_step = 5
            return

        hp_before = self.player_battle_hp
        self.player_battle_hp = max(0, self.player_battle_hp - wild_move_power)
        damage_taken = hp_before - self.player_battle_hp
        if damage_taken > 0:
            self.add_floating_text(f"-{damage_taken} HP", (238, 294), (212, 52, 52))
        if self.player_battle_hp == 0 and self.in_wild_battle:
            self.battle_message = f"Wild {wild_name} used {wild_move_name}!\nYou rushed back to safety."
            self.event_step = 6
            return
        self.battle_message = f"Wild {wild_name} used {wild_move_name}!\nChoose your next move."
        self.event_step = 5

    def try_catch_wild_pokemon(self):
        """Attempt to catch the active wild Pokemon with a basic HP-based chance."""
        wild_name = self.active_wild_name.capitalize()
        hp_ratio = self.wild_battle_hp / max(1, self.wild_max_hp)
        catch_chance = 0.24 + (1.0 - hp_ratio) * 0.55 - max(0, self.active_wild_level - self.starter_level) * 0.015
        catch_chance = max(0.08, min(0.82, catch_chance))
        if random.random() <= catch_chance:
            self.discover_pokemon(self.active_wild_name)
            if self.active_wild_name not in self.party_pokemon:
                self.party_pokemon.append(self.active_wild_name)
            self.battle_message = f"You threw a Poke Ball!\nGotcha! {wild_name} was caught!"
            self.event_step = 6
        else:
            self.battle_message = f"You threw a Poke Ball!\n{wild_name} broke free!"
            self.event_step = 4

    def use_selected_battle_bag_item(self):
        items = ["Potion", "Poke Ball"]
        item_name = items[self.battle_bag_selection]
        count = self.bag_items.get(item_name, 0)
        if count <= 0:
            self.battle_message = f"No {item_name}s left!"
            self.event_step = 5
            self.battle_submenu = "main"
            return
        if item_name == "Potion":
            heal_amount = 12
            old_hp = self.player_battle_hp
            self.player_battle_hp = min(self.player_max_hp, self.player_battle_hp + heal_amount)
            healed = self.player_battle_hp - old_hp
            self.bag_items[item_name] -= 1
            self.battle_message = f"You used a Potion!\nRecovered {healed} HP."
            self.event_step = 4
            self.battle_submenu = "main"
            return
        if item_name == "Poke Ball":
            if not self.in_wild_battle:
                self.battle_message = "No wild Pokemon to catch!"
                self.event_step = 5
                self.battle_submenu = "main"
                return
            self.bag_items[item_name] -= 1
            self.try_catch_wild_pokemon()
            self.battle_submenu = "main"

    def switch_battle_pokemon(self):
        if not self.party_pokemon:
            self.battle_submenu = "main"
            return
        if self.battle_party_selection == self.active_party_index:
            self.battle_message = f"{self.party_pokemon[self.active_party_index].capitalize()} is already out!"
            self.event_step = 5
            self.battle_submenu = "main"
            return
        self.active_party_index = self.battle_party_selection
        new_name = self.get_active_battle_pokemon_name().capitalize()
        self.battle_message = f"Come back!\nGo, {new_name}!"
        self.event_step = 4
        self.battle_submenu = "main"
    def handle_starter_level_up(self):
        """Grant one level after the route battle and evolve if threshold is reached."""
        if not self.starter_name:
            return
        self.starter_level += 1
        self.try_starter_evolution()

    def try_starter_evolution(self):
        while self.starter_name in EVOLUTION_LEVELS:
            required_level, evolved_name = EVOLUTION_LEVELS[self.starter_name]
            if self.starter_level < required_level:
                return
            self.starter_name = evolved_name
            self.discover_pokemon(self.starter_name)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.handle_menu_input(event):
                        continue
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif self.state == STATE_TITLE:
                        self.handle_title_input(event)
                    elif self.state == STATE_TEST_REGION_PICKER:
                        self.handle_test_region_picker_input(event)
                    elif self.state == STATE_NAME_ENTRY:
                        self.handle_name_entry_input(event)
                    elif self.state == STATE_TOWN:
                        self.handle_town_input(event)
                    elif self.state == STATE_BUILDING:
                        self.handle_building_input(event)
                    elif self.state == STATE_ROUTE_EVENT:
                        self.handle_route_event_input(event)
                    elif self.state == STATE_BATTLE:
                        self.handle_battle_input(event)
                    elif self.state == STATE_NEXT_TOWN:
                        self.handle_next_town_input(event)
                    elif self.state == STATE_ROUTE_EXPLORE:
                        self.handle_route_explore_input(event)
                    elif self.state == STATE_WILD_ENCOUNTER:
                        self.handle_wild_encounter_input(event)
            
            # Draw based on current state
            if self.state == STATE_TITLE:
                self.draw_title_screen()
            elif self.state == STATE_TEST_REGION_PICKER:
                self.draw_test_region_picker()
            elif self.state == STATE_NAME_ENTRY:
                self.draw_title_screen()
                self.draw_name_entry_screen()
            elif self.state == STATE_TOWN:
                self.draw_town()
            elif self.state == STATE_BUILDING:
                self.draw_building_interior()
            elif self.state == STATE_ROUTE_EVENT:
                self.draw_route_event()
            elif self.state == STATE_BATTLE:
                self.draw_battle_scene()
            elif self.state == STATE_NEXT_TOWN:
                self.draw_next_town()

            self.draw_menu_message()
            if self.show_bag:
                self.draw_bag_overlay()
            elif self.show_pokedex:
                self.draw_pokedex_overlay()
            elif self.state == STATE_ROUTE_EXPLORE:
                self.draw_route_explore()
            elif self.state == STATE_WILD_ENCOUNTER:
                self.draw_wild_encounter()
            
            self.present_screen()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
