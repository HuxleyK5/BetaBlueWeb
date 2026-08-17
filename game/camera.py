"""Smooth, bounded camera and world/screen coordinate conversion."""

import math

from .config import CAMERA_FOLLOW_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0

    def update(self, target_pixel_x, target_pixel_y, dt=0.0, snap=False):
        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2
        desired_x = max(0, min(target_pixel_x - half_w, max(0, self.world_width - SCREEN_WIDTH)))
        desired_y = max(0, min(target_pixel_y - half_h, max(0, self.world_height - SCREEN_HEIGHT)))
        blend = 1.0 if snap or dt <= 0 else 1.0 - math.exp(-CAMERA_FOLLOW_SPEED * dt)
        self.x += (desired_x - self.x) * blend
        self.y += (desired_y - self.y) * blend

    def apply(self, rect):
        return rect.move(-round(self.x), -round(self.y))

    @property
    def offset(self):
        return -round(self.x), -round(self.y)

    def world_to_screen(self, position):
        return position[0] - self.x, position[1] - self.y

    def screen_to_world(self, position):
        return position[0] + self.x, position[1] + self.y
