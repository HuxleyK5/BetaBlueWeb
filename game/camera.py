"""Camera and viewport management for Pokemon Beta Blue."""

from .config import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0

    def update(self, target_pixel_x, target_pixel_y):
        half_w = SCREEN_WIDTH // 2
        half_h = SCREEN_HEIGHT // 2
        self.x = target_pixel_x - half_w
        self.y = target_pixel_y - half_h
        self.x = max(0, min(self.x, max(0, self.world_width - SCREEN_WIDTH)))
        self.y = max(0, min(self.y, max(0, self.world_height - SCREEN_HEIGHT)))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)
