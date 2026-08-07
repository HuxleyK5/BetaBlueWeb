"""Player system for Pokemon Beta Blue."""

import pygame

from .config import TILE_SIZE, PLAYER_START_X, PLAYER_START_Y, PLAYER_SPEED


class Player:
    def __init__(self):
        self.tile_x = PLAYER_START_X
        self.tile_y = PLAYER_START_Y
        self.pixel_x = self.tile_x * TILE_SIZE
        self.pixel_y = self.tile_y * TILE_SIZE
        self.direction = "down"
        self.moving = False
        self.move_target = (self.pixel_x, self.pixel_y)
        self.speed = PLAYER_SPEED
        self.name = ""

    def start_move(self, dx, dy, is_solid):
        if self.moving:
            return
        if dx == 0 and dy == 0:
            return
        target_x = self.tile_x + dx
        target_y = self.tile_y + dy
        if is_solid(target_x, target_y):
            return
        self.tile_x = target_x
        self.tile_y = target_y
        self.move_target = (self.tile_x * TILE_SIZE, self.tile_y * TILE_SIZE)
        self.moving = True
        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"

    def update(self):
        if not self.moving:
            return
        if self.pixel_x < self.move_target[0]:
            self.pixel_x += self.speed
            if self.pixel_x >= self.move_target[0]:
                self.pixel_x = self.move_target[0]
        elif self.pixel_x > self.move_target[0]:
            self.pixel_x -= self.speed
            if self.pixel_x <= self.move_target[0]:
                self.pixel_x = self.move_target[0]
        if self.pixel_y < self.move_target[1]:
            self.pixel_y += self.speed
            if self.pixel_y >= self.move_target[1]:
                self.pixel_y = self.move_target[1]
        elif self.pixel_y > self.move_target[1]:
            self.pixel_y -= self.speed
            if self.pixel_y <= self.move_target[1]:
                self.pixel_y = self.move_target[1]
        if (self.pixel_x, self.pixel_y) == self.move_target:
            self.moving = False

    def draw(self, surface, offset_x, offset_y):
        sprite_rect = pygame.Rect(offset_x + self.pixel_x, offset_y + self.pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (255, 100, 100), sprite_rect)
        pygame.draw.rect(surface, (0, 0, 0), sprite_rect, 2)
        eye_x = sprite_rect.x + 10
        eye_y = sprite_rect.y + 12
        pygame.draw.circle(surface, (0, 0, 0), (eye_x, eye_y), 3)
        pygame.draw.circle(surface, (0, 0, 0), (eye_x + 12, eye_y), 3)
