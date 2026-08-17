"""Input handling for Pokemon Beta Blue."""

import pygame

from .config import MAX_PLAYER_NAME_LENGTH


class InputManager:
    """Track high-level actions so gameplay code is not tied to raw events."""

    KEY_BINDINGS = {
        "move_left": (pygame.K_LEFT, pygame.K_a),
        "move_right": (pygame.K_RIGHT, pygame.K_d),
        "move_up": (pygame.K_UP, pygame.K_w),
        "move_down": (pygame.K_DOWN, pygame.K_s),
        "confirm": (pygame.K_RETURN, pygame.K_SPACE),
        "cancel": (pygame.K_ESCAPE, pygame.K_BACKSPACE),
        "fullscreen": (pygame.K_F11,),
    }

    def __init__(self):
        self.pressed = set()

    def begin_frame(self):
        self.pressed.clear()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.pressed.update(action for action, keys in self.KEY_BINDINGS.items() if event.key in keys)

    def was_pressed(self, action):
        return action in self.pressed

    def movement_vector(self):
        return get_movement_vector(pygame.key.get_pressed())


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
