"""Window and screen scaling for Pokemon Beta Blue."""

import pygame

from .config import SCREEN_WIDTH, SCREEN_HEIGHT


class GameWindow:
    def __init__(self, fullscreen=True):
        self.fullscreen = fullscreen
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN if fullscreen else 0)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokemon Beta Blue")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def present(self):
        window_width, window_height = self.window.get_size()
        pygame.transform.scale(self.screen, (window_width, window_height), self.window)
        pygame.display.flip()
