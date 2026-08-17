"""Window and screen scaling for Pokemon Beta Blue."""

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH, Settings


class GameWindow:
    """Own the OS window and scale a fixed-resolution game canvas into it."""

    def __init__(self, settings=None):
        settings = settings or Settings()
        self.fullscreen = settings.fullscreen
        self.windowed_size = (settings.window_width, settings.window_height)
        self.vsync = settings.vsync
        self.window = self._create_window()
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokemon Beta Blue")

    def _create_window(self):
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        size = (0, 0) if self.fullscreen else self.windowed_size
        try:
            return pygame.display.set_mode(size, flags, vsync=int(self.vsync))
        except pygame.error:
            return pygame.display.set_mode(size, flags)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.window = self._create_window()

    def present(self):
        window_width, window_height = self.window.get_size()
        scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
        target_size = (max(1, int(SCREEN_WIDTH * scale)), max(1, int(SCREEN_HEIGHT * scale)))
        target = pygame.Rect(0, 0, *target_size)
        target.center = (window_width // 2, window_height // 2)
        self.window.fill((0, 0, 0))
        pygame.transform.scale(self.screen, target_size, self.window.subsurface(target))
        pygame.display.flip()
