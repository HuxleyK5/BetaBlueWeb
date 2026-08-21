"""User interface widgets and text utilities."""

import pygame

from .config import SCREEN_WIDTH, SCREEN_HEIGHT
from .theme import draw_meter, draw_panel as draw_themed_panel


def render_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    return rect


def draw_panel(surface, rect, fill_color=(20, 22, 40), border_color=(220, 220, 220), border_width=2):
    draw_themed_panel(surface, rect, fill_color, border_color, border_width, 8)


def draw_health_bar(surface, x, y, width, height, current, maximum, fill_color=(90, 210, 90), back_color=(50, 50, 70), border_color=(200, 200, 220)):
    ratio = current / maximum if maximum > 0 else 0
    draw_meter(surface, (x, y, width, height), ratio, fill_color)


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
