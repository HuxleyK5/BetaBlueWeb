"""Deterministic world clock, seasons, and changing regional weather."""

from dataclasses import dataclass
import random

SEASONS = ("spring", "summer", "autumn", "winter")
WEATHER = ("clear", "sunny", "rain", "fog", "storm", "snow")


@dataclass
class WorldSimulation:
    """World time advances independently from rendering and is fully saveable."""

    total_minutes: float = 8 * 60
    weather: str = "clear"
    weather_minutes_remaining: float = 120.0
    seed: int = 1337
    minutes_per_second: float = 4.0
    season_length_days: int = 3

    @property
    def day(self):
        return int(self.total_minutes // 1440) + 1

    @property
    def hour(self):
        return (self.total_minutes % 1440) / 60

    @property
    def time_of_day(self):
        if 5 <= self.hour < 8:
            return "dawn"
        if 8 <= self.hour < 18:
            return "day"
        if 18 <= self.hour < 21:
            return "dusk"
        return "night"

    @property
    def clock_text(self):
        hour = int(self.hour)
        minute = int((self.hour - hour) * 60)
        return f"{hour:02d}:{minute:02d}"

    @property
    def season(self):
        return SEASONS[((self.day - 1) // self.season_length_days) % len(SEASONS)]

    def update(self, dt):
        advanced = max(0.0, dt) * self.minutes_per_second
        self.total_minutes += advanced
        self.weather_minutes_remaining -= advanced
        if self.weather_minutes_remaining <= 0:
            self._choose_weather()

    def advance_hours(self, hours):
        advanced = max(0, hours) * 60
        self.total_minutes += advanced
        self.weather_minutes_remaining -= advanced
        if self.weather_minutes_remaining <= 0:
            self._choose_weather()

    def _choose_weather(self):
        seasonal = {
            "spring": (("clear", 4), ("rain", 4), ("fog", 2), ("storm", 1)),
            "summer": (("sunny", 5), ("clear", 4), ("rain", 1), ("storm", 1)),
            "autumn": (("clear", 4), ("fog", 3), ("rain", 3), ("storm", 1)),
            "winter": (("snow", 5), ("clear", 3), ("fog", 2), ("storm", 1)),
        }[self.season]
        rng = random.Random(self.seed + int(self.total_minutes // 120))
        names, weights = zip(*seasonal)
        self.weather = rng.choices(names, weights=weights, k=1)[0]
        self.weather_minutes_remaining = rng.randint(90, 180)

    def to_dict(self):
        return {"total_minutes": self.total_minutes, "weather": self.weather, "weather_minutes_remaining": self.weather_minutes_remaining, "seed": self.seed}

    def restore(self, data):
        total = data.get("total_minutes", self.total_minutes)
        remaining = data.get("weather_minutes_remaining", self.weather_minutes_remaining)
        weather = data.get("weather", self.weather)
        seed = data.get("seed", self.seed)
        if not isinstance(total, (int, float)) or total < 0 or not isinstance(remaining, (int, float)):
            raise ValueError("invalid saved world clock")
        if weather not in WEATHER and weather != "starfall":
            raise ValueError("invalid saved weather")
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise ValueError("invalid world seed")
        self.total_minutes, self.weather_minutes_remaining, self.weather, self.seed = total, remaining, weather, seed
