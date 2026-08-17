"""Capture probability, shake resolution, and animation state."""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class CaptureContext:
    rarity: str = "common"
    zone: str = "grass"
    time_of_day: str = "day"
    legendary_event: bool = False


@dataclass(frozen=True)
class CaptureResult:
    success: bool
    shakes: int
    chance: float
    blocked_reason: str = ""


@dataclass
class CaptureAnimation:
    result: CaptureResult
    ball_id: str
    elapsed: float = 0.0
    duration: float = 2.4

    @property
    def complete(self):
        return self.elapsed >= self.duration

    @property
    def progress(self):
        return min(1.0, self.elapsed / self.duration)

    @property
    def visible_shakes(self):
        return min(self.result.shakes, max(0, int((self.elapsed - 0.8) / 0.35) + 1))

    def update(self, dt):
        self.elapsed = min(self.duration, self.elapsed + dt)


class CaptureCalculator:
    """Resolve captures from species rate, health, status, ball, and context."""

    def __init__(self, rng=None):
        self.rng = rng or random.Random()

    def attempt(self, pokemon, ball, context=None):
        context = context or CaptureContext()
        if ball.category != "ball":
            return CaptureResult(False, 0, 0.0, "That item is not a Poké Ball.")
        if context.rarity == "legendary" and not context.legendary_event:
            return CaptureResult(False, 0, 0.0, "A special legendary encounter is required.")

        modifier = self._ball_modifier(ball, pokemon, context)
        if ball.item_id == "master_ball":
            return CaptureResult(True, 4, 1.0)
        status_modifier = 2.5 if pokemon.status in {"sleep", "freeze"} else 1.5 if pokemon.status in {"burn", "poison", "paralysis"} else 1.0
        health_factor = (3 * pokemon.max_hp - 2 * pokemon.current_hp) / (3 * pokemon.max_hp)
        chance = max(1 / 255, min(0.95, health_factor * pokemon.species.catch_rate * modifier * status_modifier / 255))
        shake_chance = chance ** 0.25
        shakes = 0
        for _ in range(4):
            if self.rng.random() >= shake_chance:
                break
            shakes += 1
        return CaptureResult(shakes == 4, shakes, chance)

    @staticmethod
    def _ball_modifier(ball, pokemon, context):
        if ball.item_id == "net_ball" and {"Water", "Bug"}.intersection(pokemon.species.types):
            return 3.5
        if ball.item_id == "dusk_ball" and (context.zone == "cave" or context.time_of_day == "night"):
            return 3.0
        return ball.ball_modifier
