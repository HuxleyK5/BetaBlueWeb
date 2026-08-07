"""Weather and time systems for future open-world features."""

from enum import Enum


class WeatherType(Enum):
    CLEAR = "Clear"
    RAIN = "Rain"
    FOG = "Fog"
    STORM = "Storm"


class TimeCycle(Enum):
    DAY = "Day"
    DUSK = "Dusk"
    NIGHT = "Night"
    DAWN = "Dawn"


class WorldClock:
    def __init__(self):
        self.time_counter = 0
        self.cycle = TimeCycle.DAY
        self.weather = WeatherType.CLEAR

    def update(self):
        self.time_counter += 1
        if self.time_counter % 1200 == 0:
            self._advance_cycle()

    def _advance_cycle(self):
        sequence = [TimeCycle.DAY, TimeCycle.DUSK, TimeCycle.NIGHT, TimeCycle.DAWN]
        current_index = sequence.index(self.cycle)
        self.cycle = sequence[(current_index + 1) % len(sequence)]

    def set_weather(self, weather_type: WeatherType):
        self.weather = weather_type
