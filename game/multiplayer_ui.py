"""Read-only multiplayer foundation status screen."""

import pygame
from .config import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_multiplayer_screen(surface, identity, gateway, fonts):
    _title_font, body_font, small_font = fonts
    surface.fill((18, 29, 55))
    panel = pygame.Rect(80, 55, SCREEN_WIDTH - 160, SCREEN_HEIGHT - 110)
    pygame.draw.rect(surface, (242, 247, 253), panel, border_radius=18)
    pygame.draw.rect(surface, (58, 91, 148), panel, 5, border_radius=18)
    surface.blit(body_font.render("Multiplayer Foundation", True, (39, 72, 132)), (panel.x + 28, panel.y + 24))
    lines = (
        f"Trainer: {identity.display_name}",
        f"Player ID: {identity.player_id[:12]}...",
        f"Account provider: {identity.provider}",
        f"Authenticated: {'Yes' if identity.authenticated else 'Guest / offline'}",
        f"Transport: {type(gateway.transport).__name__}",
        f"Connection state: {gateway.session.state.value.title()}",
        "",
        "Single-player remains fully available without connecting.",
        "Loopback verifies protocol messages locally; it never opens a socket.",
        "A future server can implement the same account and transport interfaces.",
    )
    for index, line in enumerate(lines):
        surface.blit(small_font.render(line, True, (48, 62, 84)), (panel.x + 35, panel.y + 85 + index * 30))
    hint = "ENTER: connect/disconnect loopback   M/ESC: close"
    surface.blit(small_font.render(hint, True, (81, 96, 118)), (panel.x + 28, panel.bottom - 38))
