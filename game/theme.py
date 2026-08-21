"""Shared visual language for the polished handheld-RPG presentation."""

import pygame


INK = (29, 42, 59)
PAPER = (250, 250, 239)
PAPER_SHADE = (222, 232, 227)
BLUE = (48, 105, 183)
BLUE_LIGHT = (103, 165, 224)
GOLD = (247, 201, 66)
SHADOW = (17, 31, 47, 105)
STATUS_COLORS = {
    "healthy": (73, 181, 92), "burn": (224, 86, 43), "poison": (154, 75, 174),
    "paralysis": (225, 187, 47), "sleep": (98, 121, 179), "freeze": (92, 190, 218),
}


def draw_gradient(surface, top, bottom, step=8):
    """Draw a cheap banded gradient that suits pixel-art presentation."""
    width, height = surface.get_size()
    for y in range(0, height, step):
        ratio = y / max(1, height - step)
        color = tuple(round(a + (b - a) * ratio) for a, b in zip(top, bottom))
        pygame.draw.rect(surface, color, (0, y, width, step))


def draw_panel(surface, rect, fill=PAPER, border=INK, border_width=3, radius=10, shadow=True):
    rect = pygame.Rect(rect)
    if shadow:
        shadow_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW, (5, 6, rect.width, rect.height), border_radius=radius)
        surface.blit(shadow_surface, (rect.x - 5, rect.y - 5))
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)
    if rect.height > 10:
        pygame.draw.line(surface, (255, 255, 255), (rect.x + radius, rect.y + 4), (rect.right - radius, rect.y + 4), 2)
        pygame.draw.line(surface, PAPER_SHADE, (rect.x + radius, rect.bottom - 4), (rect.right - radius, rect.bottom - 4), 2)


def draw_button(surface, rect, selected=False, color=BLUE):
    rect = pygame.Rect(rect)
    fill = color if selected else (222, 232, 238)
    border = GOLD if selected else (93, 113, 129)
    draw_panel(surface, rect, fill, border, 3 if selected else 2, 8, shadow=selected)
    if selected:
        pygame.draw.polygon(surface, GOLD, [(rect.x - 10, rect.centery), (rect.x - 3, rect.centery - 6), (rect.x - 3, rect.centery + 6)])


def draw_badge(surface, text, font, rect, color):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, color, rect, border_radius=rect.height // 2)
    pygame.draw.rect(surface, INK, rect, 2, border_radius=rect.height // 2)
    label = font.render(text, True, (255, 255, 255))
    surface.blit(label, label.get_rect(center=rect.center))


def draw_meter(surface, rect, ratio, fill, label=None, font=None):
    rect = pygame.Rect(rect)
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(surface, (49, 61, 69), rect, border_radius=rect.height // 2)
    inner = rect.inflate(-4, -4)
    pygame.draw.rect(surface, (22, 31, 39), inner, border_radius=inner.height // 2)
    width = round(inner.width * ratio)
    if width:
        bar = pygame.Rect(inner.x, inner.y, width, inner.height)
        pygame.draw.rect(surface, fill, bar, border_radius=inner.height // 2)
        highlight = pygame.Rect(bar.x + 2, bar.y + 2, max(0, bar.width - 4), max(1, bar.height // 3))
        pygame.draw.rect(surface, tuple(min(255, value + 45) for value in fill), highlight, border_radius=highlight.height // 2)
    if label and font:
        rendered = font.render(label, True, (247, 250, 245))
        surface.blit(rendered, (rect.x - rendered.get_width() - 6, rect.centery - rendered.get_height() // 2))
