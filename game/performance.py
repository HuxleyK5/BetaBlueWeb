"""Small opt-in runtime diagnostics overlay."""

from collections import deque
import pygame


class PerformanceMonitor:
    def __init__(self, sample_count=120):
        self.visible = False
        self.frame_times = deque(maxlen=sample_count)

    def record(self, dt):
        if dt > 0:
            self.frame_times.append(dt * 1000)

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface, font, asset_manager):
        if not self.visible:
            return
        average = sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0
        fps = 1000 / average if average else 0
        stats = asset_manager.cache_stats()
        lines = (f"FPS {fps:5.1f}   Frame {average:5.2f} ms", f"Cached images {stats['images']}   fonts {stats['fonts']}")
        panel = pygame.Surface((310, 55), pygame.SRCALPHA); panel.fill((5, 10, 24, 220))
        for index, line in enumerate(lines):
            panel.blit(font.render(line, True, (170, 245, 190)), (9, 6 + index * 23))
        surface.blit(panel, (surface.get_width() - panel.get_width() - 8, 42))
