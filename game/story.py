"""Story progression and badge systems."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Badge:
    badge_id: str
    name: str
    description: str


class StoryProgress:
    def __init__(self):
        self.active_chapter = "beta_region"
        self.badges: List[Badge] = []
        self.flags: Dict[str, bool] = {}

    def earn_badge(self, badge: Badge):
        if badge.badge_id not in [b.badge_id for b in self.badges]:
            self.badges.append(badge)

    def set_flag(self, key: str, value: bool = True):
        self.flags[key] = value

    def check_flag(self, key: str):
        return self.flags.get(key, False)
