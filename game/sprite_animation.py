"""Sprite presentation helpers that animate existing transparent pixel art."""

import math

import pygame

from .theme import STATUS_COLORS


def draw_creature(surface, sprite, center, status="healthy", phase_offset=0.0, scale=1.0, flipped=False):
    """Draw a breathing, bobbing creature while preserving nearest-neighbor pixels."""
    ticks = pygame.time.get_ticks() / 1000.0 + phase_offset
    bob = round(math.sin(ticks * 3.2) * 4)
    breathe = 1.0 + math.sin(ticks * 2.4) * 0.018
    width = max(1, round(sprite.get_width() * scale * breathe))
    height = max(1, round(sprite.get_height() * scale / breathe))
    frame = pygame.transform.scale(sprite, (width, height))
    if flipped:
        frame = pygame.transform.flip(frame, True, False)
    center = (round(center[0]), round(center[1] + bob))
    shadow_width = round(width * (0.48 - bob * 0.004))
    shadow = pygame.Surface((max(1, shadow_width), 18), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (18, 36, 42, 105), shadow.get_rect())
    surface.blit(shadow, shadow.get_rect(center=(center[0], center[1] + height // 2 - 5)))
    surface.blit(frame, frame.get_rect(center=center))
    draw_status_particles(surface, center, status, ticks, max(18, width // 3))


def draw_status_particles(surface, center, status, ticks, radius):
    if status == "healthy":
        return
    color = STATUS_COLORS.get(status, (220, 220, 220))
    for index in range(4):
        angle = ticks * 2.2 + index * math.pi / 2
        x = round(center[0] + math.cos(angle) * radius)
        y = round(center[1] + math.sin(angle) * radius * 0.55 - radius)
        if status == "sleep":
            pygame.draw.line(surface, color, (x - 3, y - 3), (x + 3, y - 3), 2)
            pygame.draw.line(surface, color, (x + 3, y - 3), (x - 3, y + 3), 2)
            pygame.draw.line(surface, color, (x - 3, y + 3), (x + 3, y + 3), 2)
        else:
            pygame.draw.circle(surface, color, (x, y), 3 + index % 2)
