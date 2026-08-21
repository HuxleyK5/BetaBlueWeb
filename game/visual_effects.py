"""Reusable presentation-only animation controllers for battles and travel."""

from dataclasses import dataclass
import math

import pygame

from .config import SCREEN_HEIGHT, SCREEN_WIDTH


@dataclass
class MoveVisual:
    move_key: str
    type_name: str
    from_side: str
    damage: int = 0
    elapsed: float = 0.0
    duration: float = 0.78

    @property
    def progress(self):
        return min(1.0, self.elapsed / self.duration)

    @property
    def complete(self):
        return self.elapsed >= self.duration


class BattleAnimator:
    """Queue battle presentation without delaying or changing battle rules."""

    SOURCE_POSITIONS = {"player": (235, 345), "enemy": (585, 165)}

    def __init__(self):
        self.intro_elapsed = 0.0
        self.intro_duration = 0.9
        self.intro_active = False
        self.queue = []
        self.active = None

    @property
    def busy(self):
        return self.intro_active or self.active is not None or bool(self.queue)

    def start_intro(self):
        self.intro_elapsed = 0.0
        self.intro_active = True
        self.queue.clear()
        self.active = None

    def play_move(self, move, from_side, damage=0):
        self.queue.append(MoveVisual(move.key, move.type_name, from_side, max(0, damage)))
        if self.active is None and not self.intro_active:
            self.active = self.queue.pop(0)

    def update(self, dt):
        if self.intro_active:
            self.intro_elapsed += dt
            if self.intro_elapsed >= self.intro_duration:
                self.intro_active = False
            return
        if self.active is None and self.queue:
            self.active = self.queue.pop(0)
        if self.active is not None:
            self.active.elapsed += dt
            if self.active.complete:
                self.active = None
                if self.queue:
                    self.active = self.queue.pop(0)

    def sprite_offset(self, side):
        if self.intro_active:
            progress = self._ease_out(min(1.0, self.intro_elapsed / self.intro_duration))
            return (int((1 - progress) * (-250 if side == "player" else 250)), 0)
        effect = self.active
        if effect is None:
            return (0, 0)
        progress = effect.progress
        target_side = "enemy" if effect.from_side == "player" else "player"
        if side == effect.from_side and progress < 0.48 and effect.type_name in {"Normal", "Fighting", "Flying", "Steel", "Dark", "Bug"}:
            strength = math.sin(progress / 0.48 * math.pi) * 28
            return (round(strength if side == "player" else -strength), round(-strength * 0.35))
        if side == target_side and 0.55 < progress < 0.9 and effect.damage:
            return (round(math.sin(progress * 70) * 6), 0)
        return (0, 0)

    def sprite_visible(self, side):
        effect = self.active
        if effect is None:
            return True
        target = "enemy" if effect.from_side == "player" else "player"
        return not (side == target and effect.damage and 0.62 < effect.progress < 0.84 and int(effect.progress * 28) % 2 == 0)

    def draw(self, surface, font):
        effect = self.active
        if effect is None:
            return
        progress = effect.progress
        source = self.SOURCE_POSITIONS[effect.from_side]
        target_side = "enemy" if effect.from_side == "player" else "player"
        target = self.SOURCE_POSITIONS[target_side]
        move = effect.move_key
        type_name = effect.type_name

        if type_name == "Fire":
            self._projectiles(surface, source, target, progress, (255, 111, 34), (255, 225, 96), arc=38)
        elif type_name == "Water":
            self._stream(surface, source, target, progress, (81, 194, 246), (205, 246, 255))
        elif type_name == "Grass":
            self._orbiting_orbs(surface, source if "drain" not in move and move != "absorb" else target, target if "drain" not in move and move != "absorb" else source, progress, (91, 208, 91))
        elif type_name == "Ground":
            self._projectiles(surface, source, target, progress, (145, 99, 55), (205, 154, 83), arc=24)
        elif type_name == "Psychic":
            for index in range(4):
                radius = round(12 + progress * 58 + index * 9)
                pygame.draw.circle(surface, (212, 91 + index * 18, 211), target, radius, 2)
        elif type_name == "Poison":
            self._projectiles(surface, source, target, progress, (151, 65, 174), (226, 120, 225), arc=28)
        elif type_name in {"Flying", "Steel"} or move in {"scratch", "leaf_blade"}:
            color = (225, 245, 255) if type_name == "Steel" else (255, 242, 175)
            for offset in (-15, 0, 15):
                spread = round(28 * math.sin(progress * math.pi))
                pygame.draw.line(surface, color, (target[0] - spread, target[1] + offset - 12), (target[0] + spread, target[1] + offset + 12), 4)
        elif type_name == "Dark" or move == "bite":
            gap = round(30 - 20 * math.sin(progress * math.pi))
            pygame.draw.arc(surface, (55, 49, 71), (target[0] - 35, target[1] - gap - 22, 70, 45), 3.2, 6.2, 7)
            pygame.draw.arc(surface, (55, 49, 71), (target[0] - 35, target[1] + gap - 22, 70, 45), 0.1, 3.0, 7)
        elif type_name == "Bug":
            self._orbiting_orbs(surface, source, target, progress, (174, 199, 56))
        elif move in {"growl", "leer", "string_shot", "sand_attack"}:
            for index in range(4):
                pygame.draw.circle(surface, (255, 232, 148), source, round(15 + progress * 65 + index * 12), 2)
        else:
            radius = max(5, round(32 * math.sin(progress * math.pi)))
            pygame.draw.circle(surface, (255, 239, 145), target, radius, 4)
            pygame.draw.line(surface, (255, 255, 245), (target[0] - radius, target[1]), (target[0] + radius, target[1]), 3)

        if effect.damage and progress > 0.58:
            rise = round((progress - 0.58) * 75)
            text = font.render(f"-{effect.damage}", True, (225, 48, 48))
            surface.blit(text, text.get_rect(center=(target[0], target[1] - 65 - rise)))

    @staticmethod
    def _projectiles(surface, source, target, progress, outer, inner, arc=0):
        for index in range(7):
            travel = max(0.0, min(1.0, progress * 1.35 - index * 0.07))
            x = round(source[0] + (target[0] - source[0]) * travel)
            y = round(source[1] + (target[1] - source[1]) * travel - arc * 4 * travel * (1 - travel))
            pygame.draw.circle(surface, outer, (x, y), 7 - index // 3)
            pygame.draw.circle(surface, inner, (x, y), 3)

    @staticmethod
    def _stream(surface, source, target, progress, outer, inner):
        end_t = min(1.0, progress * 1.35)
        points = []
        for index in range(15):
            travel = max(0.0, end_t - index * 0.035)
            x = round(source[0] + (target[0] - source[0]) * travel)
            y = round(source[1] + (target[1] - source[1]) * travel + math.sin(index + progress * 20) * 7)
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.lines(surface, outer, False, points, 8)
            pygame.draw.lines(surface, inner, False, points, 3)

    @staticmethod
    def _orbiting_orbs(surface, source, target, progress, color):
        for index in range(6):
            travel = max(0.0, min(1.0, progress * 1.25 - index * 0.06))
            x = source[0] + (target[0] - source[0]) * travel
            y = source[1] + (target[1] - source[1]) * travel
            angle = progress * 14 + index * 1.05
            pygame.draw.ellipse(surface, color, (round(x + math.cos(angle) * 14) - 6, round(y + math.sin(angle) * 10) - 3, 12, 6))

    @staticmethod
    def _ease_out(value):
        return 1 - (1 - value) ** 3


class TransitionFade:
    """Short fade-in overlay used after connected-area travel."""

    def __init__(self):
        self.elapsed = 1.0
        self.duration = 0.55

    @property
    def active(self):
        return self.elapsed < self.duration

    def start(self):
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed = min(self.duration, self.elapsed + dt)

    def draw(self, surface):
        if not self.active:
            return
        alpha = round(255 * (1 - self.elapsed / self.duration) ** 2)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((7, 22, 45, alpha))
        surface.blit(overlay, (0, 0))


class FeedbackBurst:
    """Small reusable sparkle burst for healing, captures, and level gains."""

    def __init__(self):
        self.elapsed = 1.0
        self.duration = 0.9
        self.text = ""
        self.color = (110, 224, 135)

    @property
    def active(self):
        return self.elapsed < self.duration

    def start(self, text, color):
        self.elapsed = 0.0
        self.text = text
        self.color = color

    def update(self, dt):
        self.elapsed = min(self.duration, self.elapsed + dt)

    def draw(self, surface, font):
        if not self.active:
            return
        progress = self.elapsed / self.duration
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        for index in range(12):
            angle = index * math.tau / 12
            distance = 20 + progress * 95
            point = (round(center[0] + math.cos(angle) * distance), round(center[1] + math.sin(angle) * distance))
            radius = max(1, round(5 * (1 - progress)))
            pygame.draw.circle(surface, self.color, point, radius)
            pygame.draw.line(surface, (255, 255, 235), (point[0] - radius - 2, point[1]), (point[0] + radius + 2, point[1]), 1)
        label = font.render(self.text, True, self.color)
        backing = label.get_rect(center=(center[0], center[1] - round(progress * 35))).inflate(24, 14)
        veil = pygame.Surface(backing.size, pygame.SRCALPHA)
        veil.fill((21, 37, 55, round(220 * (1 - progress))))
        surface.blit(veil, backing)
        label.set_alpha(round(255 * (1 - progress)))
        surface.blit(label, label.get_rect(center=backing.center))
