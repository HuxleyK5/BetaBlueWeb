"""Lightweight procedural lighting and weather overlays."""

import math
import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH


def draw_world_effects(surface, simulation, context):
    """Render seasonal tint, daylight, then weather without external assets."""
    season_colors = {"spring": (110, 180, 120, 12), "summer": (255, 215, 90, 10), "autumn": (205, 112, 55, 18), "winter": (185, 215, 245, 20)}
    tint = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    tint.fill(season_colors[simulation.season])
    surface.blit(tint, (0, 0))

    darkness = {"dawn": 55, "day": 0, "dusk": 75, "night": 145}[simulation.time_of_day]
    if darkness:
        light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        light.fill((10, 18, 55, darkness))
        surface.blit(light, (0, 0))

    ticks = int(simulation.total_minutes * 3)
    weather = context.weather
    if weather in {"rain", "storm"}:
        count = 90 if weather == "storm" else 55
        for index in range(count):
            x = (index * 83 + ticks * 5) % (SCREEN_WIDTH + 40) - 20
            y = (index * 47 + ticks * 9) % (SCREEN_HEIGHT + 40) - 20
            pygame.draw.line(surface, (170, 210, 245), (x, y), (x - 7, y + 16), 2)
    elif weather == "snow":
        for index in range(60):
            x = (index * 97 + ticks) % SCREEN_WIDTH
            y = (index * 53 + ticks * 2) % SCREEN_HEIGHT
            pygame.draw.circle(surface, (242, 248, 255), (x, y), 2 + index % 2)
    elif weather == "fog":
        fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fog.fill((215, 224, 225, 90))
        surface.blit(fog, (0, 0))
    elif weather == "starfall":
        for index in range(34):
            x = (index * 137 + ticks // 2) % SCREEN_WIDTH
            y = (index * 61 + int(8 * math.sin((ticks + index) / 15))) % (SCREEN_HEIGHT - 80)
            pygame.draw.circle(surface, (255, 241, 145), (x, y), 2)
            if index % 7 == 0:
                pygame.draw.line(surface, (255, 245, 185), (x, y), (x - 12, y + 8), 1)
