"""
Beta Blue - A Pokemon-style top-down RPG scene.
A 2D handheld-inspired RPG with a title screen, name entry, and town exploration.
"""

import pygame
import sys
from pathlib import Path

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
MAP_WIDTH = 20
MAP_HEIGHT = 15

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

# Game States
STATE_TITLE = "title"
STATE_NAME_ENTRY = "name_entry"
STATE_TOWN = "town"
STATE_BUILDING = "building"
STATE_ROUTE_EVENT = "route_event"

# Map tiles
TILE_GRASS = 0
TILE_PATH = 1
TILE_BUILDING = 2
TILE_TREE = 3
TILE_WATER = 4

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
EVENT_POKEMON = STARTER_NAMES + ["poochyena"]
ROUTE_ASSIST_TILE = (10, 1)
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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Beta Blue")
        self.clock = pygame.time.Clock()
        
        self.state = STATE_TITLE
        self.player_name = ""
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
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
        self.professor_rescued = False
        self.current_building = None

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
        pixel_x = x * TILE_SIZE
        pixel_y = y * TILE_SIZE
        
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

    def draw_building(self, building):
        """Draw one enterable building as a single readable landmark."""
        x = building["x"] * TILE_SIZE
        y = building["y"] * TILE_SIZE
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
        door_x = building["door"][0] * TILE_SIZE + 6
        door_y = building["door"][1] * TILE_SIZE - 30
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
        self.draw_rounded_rect(box, UI_PANEL, radius=12, outline_color=OUTLINE, outline_width=4)
        for index, line in enumerate(lines):
            text = self.font_medium.render(line, True, OUTLINE)
            self.screen.blit(text, (box.x + 24, box.y + 18 + index * 28))
        prompt_text = self.font_small.render(prompt, True, TEXT_BLUE)
        prompt_rect = prompt_text.get_rect(right=box.right - 24, bottom=box.bottom - 14)
        self.screen.blit(prompt_text, prompt_rect)
    
    def draw_player(self):
        """Draw the player character"""
        pixel_x = self.player_x * TILE_SIZE
        pixel_y = self.player_y * TILE_SIZE
        
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
        self.screen.fill((67, 155, 217))
        
        # Animated ocean-and-route pattern
        self.title_timer += 1
        pygame.draw.rect(self.screen, (114, 209, 128), (0, 360, SCREEN_WIDTH, 240))
        pygame.draw.rect(self.screen, PATH, (0, 420, SCREEN_WIDTH, 80), border_radius=12)
        for i in range(-80, SCREEN_WIDTH + 80, 80):
            wave_y = 80 + ((i + self.title_timer) % 60)
            pygame.draw.arc(self.screen, WATER_LIGHT, (i, wave_y, 72, 28), 0, 3.14, 3)
        
        # Title
        shadow = self.font_title.render("Beta Blue", True, OUTLINE)
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 88))
        self.screen.blit(shadow, shadow_rect)
        title_text = self.font_title.render("Beta Blue", True, TEXT_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 92))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Sapphire Shore Adventure", True, TEXT_WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 35))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Start prompt (blinking)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start_text = self.font_large.render("Press ENTER", True, TEXT_WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 68))
            self.screen.blit(start_text, start_rect)
        
        # Credits
        credits_text = self.font_small.render("Use Arrow Keys to Move", True, (238, 251, 255))
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(credits_text, credits_rect)
    
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

        # Draw player
        self.draw_player()

        building = self.get_building_at_player()
        if building:
            self.draw_dialog_box([f"Enter {building['name']}?", "Press ENTER to go inside."], "ENTER")
        elif self.player_at_route_assist() and not self.professor_rescued:
            if self.starter_name:
                self.draw_dialog_box(["You hear the professor shouting up ahead!", "Press ENTER to help on the northern route."], "ENTER")
            else:
                self.draw_dialog_box(["Tall grass blocks the northern route.", "Visit the lab and choose a starter first."], "ENTER")
        elif self.player_at_route_assist() and self.professor_rescued:
            starter = self.starter_name.capitalize() if self.starter_name else "starter"
            self.draw_dialog_box([f"The northern route is calm again.", f"{starter} waits for the next challenge."], "ENTER")
        
        # Draw player name above player
        if self.player_name:
            name_label = self.font_small.render(self.player_name, True, TEXT_WHITE)
            label_x = self.player_x * TILE_SIZE + TILE_SIZE // 2
            label_y = self.player_y * TILE_SIZE - 5
            label_rect = name_label.get_rect(center=(label_x, label_y))
            
            # Background for name
            bg_rect = label_rect.copy()
            bg_rect.inflate_ip(4, 2)
            pygame.draw.rect(self.screen, OUTLINE, bg_rect, border_radius=4)
            self.screen.blit(name_label, label_rect)

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
            if not self.starter_name:
                self.draw_starter_selection()
            else:
                starter = self.starter_name.capitalize()
                self.draw_dialog_box([f"{starter}'s Pokeball is registered to you.", "Head north to assist Professor Birch."], "ESC to leave")
        else:
            pygame.draw.rect(self.screen, (224, 174, 111), (134, 166, 170, 50), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (134, 166, 170, 50), 3, border_radius=8)
            pygame.draw.rect(self.screen, (126, 84, 58), (506, 150, 92, 130), border_radius=8)
            pygame.draw.rect(self.screen, OUTLINE, (506, 150, 92, 130), 3, border_radius=8)
            self.draw_dialog_box(building["message"], "ESC to leave")

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
        pygame.draw.circle(self.screen, (239, 214, 191), (394, 210), 17)
        pygame.draw.rect(self.screen, (94, 171, 230), (378, 226, 32, 46), border_radius=8)
        professor_label = self.font_small.render("PROF.", True, OUTLINE)
        self.screen.blit(professor_label, (374, 278))

        wild = self.pokemon_sprites.get("poochyena")
        if wild:
            wild_rect = wild.get_rect(midbottom=(480, 300))
            pygame.draw.ellipse(self.screen, (161, 120, 76), (wild_rect.x + 3, wild_rect.bottom - 8, wild_rect.width - 6, 8))
            self.screen.blit(wild, wild_rect)
        wild_label = self.font_small.render("Wild Poochyena", True, OUTLINE)
        self.screen.blit(wild_label, (430, 306))

        if self.event_step == 0:
            self.draw_dialog_box(["Professor Birch: Help! A wild Pokemon", "cornered me while I checked my notes!"])
        elif self.event_step == 1:
            starter = self.starter_name.capitalize()
            sprite = self.pokemon_sprites.get(self.starter_name)
            if sprite:
                rect = sprite.get_rect(midbottom=(318, 304))
                self.screen.blit(sprite, rect)
            self.draw_dialog_box([f"{starter}, I choose you!", f"{starter} drove the wild Pokemon away!"])
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
            self.state = STATE_BUILDING
            return

        if event.key == pygame.K_RETURN and self.player_at_route_assist():
            if self.starter_name and not self.professor_rescued:
                self.state = STATE_ROUTE_EVENT
                self.event_step = 0
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
        elif event.key == pygame.K_RETURN:
            self.state = STATE_TOWN
            self.current_building = None

    def handle_route_event_input(self, event):
        """Advance the northern route rescue event."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_TOWN
            return

        if event.key == pygame.K_RETURN:
            if self.event_step == 0:
                self.event_step = 1
            elif self.event_step == 1:
                self.event_step = 2
            else:
                self.professor_rescued = True
                self.state = STATE_TOWN
                self.player_x, self.player_y = ROUTE_ASSIST_TILE
                self.player_direction = "down"
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.state == STATE_TITLE:
                        self.handle_title_input(event)
                    elif self.state == STATE_NAME_ENTRY:
                        self.handle_name_entry_input(event)
                    elif self.state == STATE_TOWN:
                        self.handle_town_input(event)
                    elif self.state == STATE_BUILDING:
                        self.handle_building_input(event)
                    elif self.state == STATE_ROUTE_EVENT:
                        self.handle_route_event_input(event)
            
            # Draw based on current state
            if self.state == STATE_TITLE:
                self.draw_title_screen()
            elif self.state == STATE_NAME_ENTRY:
                self.draw_title_screen()
                self.draw_name_entry_screen()
            elif self.state == STATE_TOWN:
                self.draw_town()
            elif self.state == STATE_BUILDING:
                self.draw_building_interior()
            elif self.state == STATE_ROUTE_EVENT:
                self.draw_route_event()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
