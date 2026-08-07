"""User interface widgets and text utilities."""

import pygame

from .config import SCREEN_WIDTH, SCREEN_HEIGHT


def render_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    return rect


def draw_panel(surface, rect, fill_color=(20, 22, 40), border_color=(220, 220, 220), border_width=2):
    pygame.draw.rect(surface, fill_color, rect, border_radius=8)
    pygame.draw.rect(surface, border_color, rect, border_width, border_radius=8)


def draw_health_bar(surface, x, y, width, height, current, maximum, fill_color=(90, 210, 90), back_color=(50, 50, 70), border_color=(200, 200, 220)):
    pygame.draw.rect(surface, back_color, (x, y, width, height), border_radius=6)
    if maximum > 0:
        ratio = max(0, min(1.0, current / maximum))
    else:
        ratio = 0
    inner_width = int((width - 4) * ratio)
    pygame.draw.rect(surface, fill_color, (x + 2, y + 2, inner_width, height - 4), border_radius=6)
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2, border_radius=6)


def wrap_text(text, font, max_width):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        test_line = current + " " + word
        if font.size(test_line)[0] <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
