"""Quest and story progression system."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class QuestObjective:
    description: str
    completed: bool = False


@dataclass
class Quest:
    quest_id: str
    title: str
    description: str
    objectives: List[QuestObjective] = field(default_factory=list)
    reward: Dict[str, int] = field(default_factory=dict)
    active: bool = True
    completed: bool = False

    def update_objective(self, index: int, completed: bool = True):
        if 0 <= index < len(self.objectives):
            self.objectives[index].completed = completed
        self.completed = all(obj.completed for obj in self.objectives)


class QuestLog:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}

    def add_quest(self, quest: Quest):
        self.quests[quest.quest_id] = quest

    def complete_objective(self, quest_id: str, objective_index: int):
        quest = self.quests.get(quest_id)
        if quest:
            quest.update_objective(objective_index)

    def active_quests(self):
        return [quest for quest in self.quests.values() if quest.active and not quest.completed]

    def completed_quests(self):
        return [quest for quest in self.quests.values() if quest.completed]
