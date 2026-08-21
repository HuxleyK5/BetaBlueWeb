"""Player movement, animation, collision, and persistent trainer statistics."""

from dataclasses import dataclass

import pygame

from .config import PLAYER_ANIMATION_FPS, PLAYER_SPEED, PLAYER_START_X, PLAYER_START_Y, TILE_SIZE


DIRECTION_NAMES = {
    (-1, -1): "up_left",
    (0, -1): "up",
    (1, -1): "up_right",
    (-1, 0): "left",
    (1, 0): "right",
    (-1, 1): "down_left",
    (0, 1): "down",
    (1, 1): "down_right",
}


@dataclass(frozen=True)
class PlayerAppearance:
    """A compact, save-safe reference to one of the playable trainer looks."""

    gender: str = "male"
    skin: int = 0

    def __post_init__(self):
        if self.gender not in {"male", "female"}:
            raise ValueError("Player gender must be 'male' or 'female'")
        if not isinstance(self.skin, int) or isinstance(self.skin, bool) or not 0 <= self.skin < 3:
            raise ValueError("Player skin must be between 0 and 2")


# Rendering palettes deliberately live with the player presentation layer. New
# cosmetic packs can extend this table without changing movement or collision.
APPEARANCE_PALETTES = {
    ("male", 0): {"skin": (224, 163, 112), "hair": (65, 40, 25), "hair_style": "short", "outfit": (34, 35, 39), "accent": (217, 55, 35), "legs": (42, 94, 144), "headwear": "cap", "hat_color": (218, 57, 36), "backpack": (181, 132, 61)},
    ("male", 1): {"skin": (222, 158, 105), "hair": (105, 62, 24), "hair_style": "short", "outfit": (37, 38, 41), "accent": (213, 52, 32), "legs": (53, 54, 56), "headwear": "headband", "hat_color": (185, 43, 29), "backpack": (125, 75, 38)},
    ("male", 2): {"skin": (232, 185, 151), "hair": (199, 207, 213), "hair_style": "short", "outfit": (35, 36, 40), "accent": (211, 50, 32), "legs": (32, 33, 37), "headwear": "none", "hat_color": (211, 50, 32), "backpack": (45, 43, 43)},
    ("female", 0): {"skin": (220, 155, 104), "hair": (76, 45, 29), "hair_style": "ponytail", "outfit": (34, 35, 39), "accent": (218, 53, 34), "legs": (34, 112, 113), "headwear": "cap", "hat_color": (218, 57, 36), "backpack": (177, 123, 57)},
    ("female", 1): {"skin": (119, 72, 47), "hair": (44, 31, 25), "hair_style": "curly", "outfit": (226, 117, 31), "accent": (246, 221, 178), "legs": (43, 44, 46), "headwear": "cap", "hat_color": (238, 220, 180), "backpack": (65, 102, 48)},
    ("female", 2): {"skin": (235, 187, 157), "hair": (35, 29, 31), "hair_style": "bob", "outfit": (34, 35, 39), "accent": (216, 48, 33), "legs": (31, 32, 36), "headwear": "cap", "hat_color": (31, 31, 34), "backpack": (42, 37, 39)},
}


@dataclass
class PlayerStats:
    """Trainer progression data kept separate from movement state."""

    name: str = ""
    money: int = 3000
    badges: int = 0
    pokemon_seen: int = 0
    pokemon_caught: int = 0
    steps_taken: int = 0
    play_time_seconds: float = 0.0


class Player:
    def __init__(self, stats=None, appearance=None):
        self.stats = stats or PlayerStats()
        self.appearance = appearance or PlayerAppearance()
        self.tile_x = PLAYER_START_X
        self.tile_y = PLAYER_START_Y
        self.position = pygame.Vector2(self.tile_x * TILE_SIZE, self.tile_y * TILE_SIZE)
        self.direction = "down"
        self.moving = False
        self.move_target = self.position.copy()
        self.speed = PLAYER_SPEED
        self.animation_frame = 0
        self.animation_elapsed = 0.0

    @property
    def name(self):
        return self.stats.name

    @name.setter
    def name(self, value):
        self.stats.name = value

    @property
    def pixel_x(self):
        return self.position.x

    @property
    def pixel_y(self):
        return self.position.y

    def set_appearance(self, gender, skin):
        self.appearance = PlayerAppearance(gender, skin)

    @property
    def center(self):
        return self.position + (TILE_SIZE / 2, TILE_SIZE / 2)

    def start_move(self, dx, dy, is_solid):
        """Begin one cardinal or diagonal tile step when its path is clear."""
        if self.moving or (dx == 0 and dy == 0):
            return False
        dx = max(-1, min(1, dx))
        dy = max(-1, min(1, dy))
        self.direction = DIRECTION_NAMES[(dx, dy)]
        target_x = self.tile_x + dx
        target_y = self.tile_y + dy
        if is_solid(target_x, target_y):
            return False
        # Prevent diagonal movement through a blocked tile corner.
        if dx and dy and (is_solid(self.tile_x + dx, self.tile_y) or is_solid(self.tile_x, self.tile_y + dy)):
            return False
        self.tile_x = target_x
        self.tile_y = target_y
        self.move_target.update(target_x * TILE_SIZE, target_y * TILE_SIZE)
        self.moving = True
        return True

    def update(self, dt):
        self.stats.play_time_seconds += dt
        if not self.moving:
            self.animation_frame = 0
            self.animation_elapsed = 0.0
            return

        distance = self.speed * dt
        if self.position.distance_to(self.move_target) <= distance:
            self.position.update(self.move_target)
            self.stats.steps_taken += 1
            self.moving = False
        else:
            self.position.move_towards_ip(self.move_target, distance)

        self.animation_elapsed += dt
        frame_time = 1.0 / PLAYER_ANIMATION_FPS
        while self.animation_elapsed >= frame_time:
            self.animation_elapsed -= frame_time
            self.animation_frame = (self.animation_frame + 1) % 4

    def teleport(self, tile_x, tile_y):
        """Place the player exactly on a tile, ready for future map transitions."""
        self.tile_x, self.tile_y = tile_x, tile_y
        self.position.update(tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        self.move_target.update(self.position)
        self.moving = False

    def draw(self, surface, offset_x=0, offset_y=0):
        """Draw the selected trainer with directional, four-frame animation."""
        x = round(offset_x + self.pixel_x)
        y = round(offset_y + self.pixel_y)
        colors = APPEARANCE_PALETTES[(self.appearance.gender, self.appearance.skin)]
        bob = -1 if self.moving and self.animation_frame in (1, 3) else 0
        stride = 2 if self.moving and self.animation_frame in (1, 2) else -2 if self.moving else 0
        facing_back = self.direction.startswith("up")
        facing_left = "left" in self.direction
        facing_right = "right" in self.direction

        pygame.draw.ellipse(surface, (35, 72, 64), (x + 8, y + 33, 24, 7))
        # Backpack, legs, jacket, and arms are layered to create a readable
        # top-down silhouette even when the sprite is only one tile tall.
        if facing_back:
            pygame.draw.rect(surface, colors["backpack"], (x + 11, y + 17 + bob, 18, 16), border_radius=4)
        pygame.draw.rect(surface, colors["legs"], (x + 12 + stride, y + 28 + bob, 7, 8), border_radius=2)
        pygame.draw.rect(surface, colors["legs"], (x + 21 - stride, y + 28 + bob, 7, 8), border_radius=2)
        pygame.draw.rect(surface, (31, 34, 41), (x + 11 + stride, y + 34, 9, 4), border_radius=2)
        pygame.draw.rect(surface, (31, 34, 41), (x + 20 - stride, y + 34, 9, 4), border_radius=2)
        pygame.draw.rect(surface, colors["outfit"], (x + 10, y + 17 + bob, 20, 15), border_radius=4)
        pygame.draw.line(surface, colors["accent"], (x + 20, y + 19 + bob), (x + 20, y + 30 + bob), 2)
        arm_shift = 2 if self.moving and self.animation_frame % 2 else 0
        pygame.draw.rect(surface, colors["skin"], (x + 7, y + 20 + bob + arm_shift, 5, 9), border_radius=2)
        pygame.draw.rect(surface, colors["skin"], (x + 28, y + 20 + bob - arm_shift, 5, 9), border_radius=2)

        head_center = (x + 20, y + 13 + bob)
        pygame.draw.circle(surface, colors["skin"], head_center, 9)
        pygame.draw.arc(surface, colors["hair"], (x + 11, y + 4 + bob, 18, 18), 0, 3.1416, 6)
        if colors["hair_style"] == "ponytail":
            pony_x = x + (29 if not facing_left else 9)
            pygame.draw.circle(surface, colors["hair"], (pony_x, y + 15 + bob), 5)
        elif colors["hair_style"] == "curly":
            pygame.draw.circle(surface, colors["hair"], (x + 11, y + 14 + bob), 4)
            pygame.draw.circle(surface, colors["hair"], (x + 29, y + 14 + bob), 4)
        elif colors["hair_style"] == "bob":
            pygame.draw.rect(surface, colors["hair"], (x + 10, y + 11 + bob, 4, 9), border_radius=2)
            pygame.draw.rect(surface, colors["hair"], (x + 26, y + 11 + bob, 4, 9), border_radius=2)
        if colors["headwear"] == "cap":
            pygame.draw.arc(surface, colors["hat_color"], (x + 10, y + 2 + bob, 20, 14), 0, 3.1416, 6)
            brim_start = x + (15 if facing_left else 19 if facing_right else 13)
            pygame.draw.line(surface, colors["hat_color"], (brim_start, y + 9 + bob), (brim_start + 12, y + 9 + bob), 3)
        elif colors["headwear"] == "headband":
            pygame.draw.line(surface, colors["hat_color"], (x + 11, y + 9 + bob), (x + 29, y + 9 + bob), 3)
        if not facing_back:
            eye_y = y + 14 + bob
            if facing_left:
                eye_positions = ((x + 14, eye_y), (x + 18, eye_y))
            elif facing_right:
                eye_positions = ((x + 22, eye_y), (x + 26, eye_y))
            else:
                eye_positions = ((x + 17, eye_y), (x + 23, eye_y))
            for eye in eye_positions:
                pygame.draw.rect(surface, (24, 27, 34), (*eye, 2, 2))
