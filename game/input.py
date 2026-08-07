"""Input handling for Pokemon Beta Blue."""

import pygame

from .config import MAX_PLAYER_NAME_LENGTH


def sanitize_name_char(event):
    if event.unicode.isalnum() or event.unicode.isspace():
        return event.unicode
    return ""


def handle_name_input(event, current_name):
    if event.key == pygame.K_BACKSPACE:
        return current_name[:-1]
    if event.key == pygame.K_RETURN:
        return current_name
    if len(current_name) < MAX_PLAYER_NAME_LENGTH:
        char = sanitize_name_char(event)
        return current_name + char
    return current_name


def get_movement_vector(keys):
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += 1
    return dx, dy
