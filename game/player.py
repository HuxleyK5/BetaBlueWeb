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
    def __init__(self, stats=None):
        self.stats = stats or PlayerStats()
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
        """Draw an animated development sprite until final art is available."""
        x = round(offset_x + self.pixel_x)
        y = round(offset_y + self.pixel_y)
        bob = -2 if self.moving and self.animation_frame in (1, 3) else 0
        pygame.draw.ellipse(surface, (35, 72, 64), (x + 7, y + TILE_SIZE - 9, TILE_SIZE - 14, 8))

        body = pygame.Rect(x + 7, y + 8 + bob, TILE_SIZE - 14, TILE_SIZE - 12)
        pygame.draw.rect(surface, (54, 112, 205), body, border_radius=8)
        pygame.draw.rect(surface, (25, 42, 70), body, 2, border_radius=8)

        stride = 3 if self.moving and self.animation_frame in (1, 2) else -3 if self.moving else 0
        pygame.draw.circle(surface, (40, 45, 62), (x + 14 + stride, y + 34), 5)
        pygame.draw.circle(surface, (40, 45, 62), (x + 26 - stride, y + 34), 5)

        direction = next(vector for vector, name in DIRECTION_NAMES.items() if name == self.direction)
        look = pygame.Vector2(direction).normalize()
        eye_center = pygame.Vector2(x + TILE_SIZE / 2, y + 17 + bob) + look * 5
        perpendicular = pygame.Vector2(-look.y, look.x) * 3
        for eye in (eye_center + perpendicular, eye_center - perpendicular):
            pygame.draw.circle(surface, (18, 24, 35), (round(eye.x), round(eye.y)), 2)
