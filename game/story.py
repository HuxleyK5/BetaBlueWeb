"""Region-level story flags, chapters, badges, and event unlocks."""


class StoryProgress:
    def __init__(self):
        self.active_chapter = "A New Journey"
        self.badges = set()
        self.flags = set()

    def earn_badge(self, name):
        before = len(self.badges)
        self.badges.add(name)
        return len(self.badges) != before

    def apply_quest_rewards(self, rewards):
        self.flags.update(rewards.get("flags", []))
        if rewards.get("chapter"):
            self.active_chapter = rewards["chapter"]

    def has_flag(self, key):
        return key in self.flags

    def to_dict(self):
        return {"active_chapter": self.active_chapter, "badges": sorted(self.badges), "flags": sorted(self.flags)}
