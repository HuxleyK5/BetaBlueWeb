"""
Pocket Adventure - A Pokemon-Style Game
A 2D top-down RPG with opening screen, name entry, and town exploration
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
MAP_WIDTH = 20
MAP_HEIGHT = 15

# Colors
GRASS = (76, 175, 80)
GRASS_DARK = (56, 155, 60)
PATH = (215, 204, 200)
WATER = (33, 150, 243)
BUILDING = (141, 110, 99)
BUILDING_ROOF = (189, 189, 189)
TREE = (34, 139, 34)
TREE_TRUNK = (101, 67, 33)
UI_BG = (44, 62, 80)
TEXT_WHITE = (255, 255, 255)
TEXT_GOLD = (255, 215, 0)
PLAYER_COLOR = (255, 100, 100)

# Game States
STATE_TITLE = "title"
STATE_NAME_ENTRY = "name_entry"
STATE_TOWN = "town"

# Map tiles
TILE_GRASS = 0
TILE_PATH = 1
TILE_BUILDING = 2
TILE_TREE = 3
TILE_WATER = 4

# Create the town map (20x15)
TOWN_MAP = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

# Add some trees and water to make the town more interesting
# We'll modify the map slightly
TOWN_MAP[2][15] = 3
TOWN_MAP[2][16] = 3
TOWN_MAP[3][15] = 3
TOWN_MAP[3][16] = 3
TOWN_MAP[10][3] = 4
TOWN_MAP[10][4] = 4
TOWN_MAP[11][3] = 4
TOWN_MAP[11][4] = 4
TOWN_MAP[12][3] = 4
TOWN_MAP[12][4] = 4

# Solid tiles that player cannot walk through
SOLID_TILES = {TILE_BUILDING, TILE_TREE, TILE_WATER}


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pocket Adventure")
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
        
    def is_solid(self, x, y):
        """Check if a tile is solid"""
        if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
            return True
        return TOWN_MAP[y][x] in SOLID_TILES
    
    def draw_tile(self, x, y, tile_type):
        """Draw a single tile"""
        pixel_x = x * TILE_SIZE
        pixel_y = y * TILE_SIZE
        
        if tile_type == TILE_GRASS:
            # Draw grass with slight variation
            color = GRASS if (x + y) % 2 == 0 else GRASS_DARK
            pygame.draw.rect(self.screen, color, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            # Add some grass detail
            if (x * 3 + y * 7) % 5 == 0:
                pygame.draw.circle(self.screen, GRASS_DARK, (pixel_x + 8, pixel_y + 8), 2)
                pygame.draw.circle(self.screen, GRASS_DARK, (pixel_x + 24, pixel_y + 20), 2)
                
        elif tile_type == TILE_PATH:
            pygame.draw.rect(self.screen, PATH, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            # Add path detail
            pygame.draw.rect(self.screen, (200, 190, 185), (pixel_x + 4, pixel_y + 4, 24, 24), 2)
            
        elif tile_type == TILE_BUILDING:
            # Building base
            pygame.draw.rect(self.screen, BUILDING, (pixel_x, pixel_y + 8, TILE_SIZE, TILE_SIZE - 8))
            # Building roof
            pygame.draw.rect(self.screen, BUILDING_ROOF, (pixel_x, pixel_y, TILE_SIZE, 12))
            # Door
            pygame.draw.rect(self.screen, (80, 60, 50), (pixel_x + 10, pixel_y + 16, 12, 16))
            
        elif tile_type == TILE_TREE:
            # Tree trunk
            pygame.draw.rect(self.screen, TREE_TRUNK, (pixel_x + 12, pixel_y + 20, 8, 12))
            # Tree foliage
            pygame.draw.circle(self.screen, TREE, (pixel_x + 16, pixel_y + 14), 14)
            pygame.draw.circle(self.screen, (28, 120, 28), (pixel_x + 12, pixel_y + 10), 8)
            pygame.draw.circle(self.screen, (28, 120, 28), (pixel_x + 20, pixel_y + 16), 8)
            
        elif tile_type == TILE_WATER:
            pygame.draw.rect(self.screen, WATER, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
            # Water shimmer
            pygame.draw.line(self.screen, (100, 180, 255), (pixel_x + 4, pixel_y + 8), (pixel_x + 12, pixel_y + 8), 2)
            pygame.draw.line(self.screen, (100, 180, 255), (pixel_x + 20, pixel_y + 20), (pixel_x + 28, pixel_y + 20), 2)
    
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
        pygame.draw.rect(self.screen, body_color, (pixel_x + 8, pixel_y + 12, 16, 14))
        
        # Head
        pygame.draw.circle(self.screen, (255, 200, 180), (pixel_x + 16, pixel_y + 10), 8)
        
        # Hair
        pygame.draw.circle(self.screen, (139, 90, 43), (pixel_x + 16, pixel_y + 6), 6)
        
        # Eyes based on direction
        eye_color = (50, 50, 50)
        if self.player_direction == "down":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 13, pixel_y + 10), 2)
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 19, pixel_y + 10), 2)
        elif self.player_direction == "up":
            pass  # No eyes visible from behind
        elif self.player_direction == "left":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 12, pixel_y + 10), 2)
        elif self.player_direction == "right":
            pygame.draw.circle(self.screen, eye_color, (pixel_x + 20, pixel_y + 10), 2)
        
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
        self.screen.fill(UI_BG)
        
        # Animated background pattern
        self.title_timer += 1
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(0, SCREEN_HEIGHT, 40):
                if (i + j + self.title_timer) % 80 < 40:
                    pygame.draw.rect(self.screen, (52, 72, 90), (i, j, 40, 40))
        
        # Title
        title_text = self.font_title.render("Pocket Adventure", True, TEXT_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("A Pokemon-Style Game", True, TEXT_WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Start prompt (blinking)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start_text = self.font_large.render("Press ENTER to Start", True, TEXT_WHITE)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(start_text, start_rect)
        
        # Credits
        credits_text = self.font_small.render("Use Arrow Keys to Move", True, (150, 150, 150))
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(credits_text, credits_rect)
    
    def draw_name_entry_screen(self):
        """Draw the name entry screen"""
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Prompt
        prompt = self.font_large.render("Enter Your Name:", True, TEXT_WHITE)
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(prompt, prompt_rect)
        
        # Name input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), input_box)
        pygame.draw.rect(self.screen, TEXT_GOLD, input_box, 3)
        
        # Display entered name
        name_text = self.font_large.render(self.player_name, True, TEXT_WHITE)
        name_rect = name_text.get_rect(center=input_box.center)
        self.screen.blit(name_text, name_rect)
        
        # Cursor
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = name_rect.right + 5
            pygame.draw.line(self.screen, TEXT_WHITE, (cursor_x, name_rect.top), (cursor_x, name_rect.bottom), 2)
        
        # Instructions
        if len(self.player_name) > 0:
            instruction = self.font_medium.render("Press ENTER to confirm", True, (150, 150, 150))
        else:
            instruction = self.font_medium.render("Type your name", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_town(self):
        """Draw the town map"""
        # Draw all tiles
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                self.draw_tile(x, y, TOWN_MAP[y][x])
        
        # Draw player
        self.draw_player()
        
        # Draw player name above player
        if self.player_name:
            name_label = self.font_small.render(self.player_name, True, TEXT_WHITE)
            label_x = self.player_x * TILE_SIZE + TILE_SIZE // 2
            label_y = self.player_y * TILE_SIZE - 5
            label_rect = name_label.get_rect(center=(label_x, label_y))
            
            # Background for name
            bg_rect = label_rect.copy()
            bg_rect.inflate_ip(4, 2)
            pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
            self.screen.blit(name_label, label_rect)
    
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
            
            # Draw based on current state
            if self.state == STATE_TITLE:
                self.draw_title_screen()
            elif self.state == STATE_NAME_ENTRY:
                self.draw_title_screen()
                self.draw_name_entry_screen()
            elif self.state == STATE_TOWN:
                self.draw_town()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()