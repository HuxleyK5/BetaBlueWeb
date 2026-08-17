"""Data-driven quests and event-based objective progression."""

from dataclasses import dataclass, field
import json
from pathlib import Path

from .items import ITEM_DATABASE

VALID_KINDS = {"main", "side", "gym", "legendary"}
VALID_EVENTS = {"starter_chosen", "talk_to_npc", "visit_area", "defeat_trainer", "earn_badge", "catch_species", "capture_count"}


class QuestDataError(ValueError):
    """Raised when quest content is invalid or has broken references."""


@dataclass(frozen=True)
class QuestObjective:
    objective_id: str
    description: str
    event: str
    target: str | None = None
    required: int = 1


@dataclass(frozen=True)
class QuestDefinition:
    quest_id: str
    title: str
    description: str
    kind: str
    chapter: str
    prerequisites: tuple[str, ...]
    objectives: tuple[QuestObjective, ...]
    rewards: dict


@dataclass
class QuestProgress:
    status: str = "locked"
    objectives: dict[str, int] = field(default_factory=dict)
    reward_claimed: bool = False


@dataclass(frozen=True)
class QuestUpdate:
    quest_id: str
    objective_id: str | None
    completed: bool = False
    activated: bool = False


class QuestManager:
    """Owns quest state; gameplay systems only publish semantic events."""

    def __init__(self, data_path, known_npcs=(), known_areas=()):
        self.data_path = Path(data_path)
        self.definitions = self._load(known_npcs, known_areas)
        self.progress = {key: QuestProgress(objectives={obj.objective_id: 0 for obj in quest.objectives}) for key, quest in self.definitions.items()}
        self._activate_available()

    def emit(self, event, target=None, amount=1):
        """Apply one gameplay event and return UI updates plus earned rewards."""
        if event not in VALID_EVENTS or amount <= 0:
            return [], []
        updates, rewards = [], []
        for quest_id, quest in self.definitions.items():
            state = self.progress[quest_id]
            if state.status != "active":
                continue
            for objective in quest.objectives:
                if objective.event != event or (objective.target is not None and objective.target != target):
                    continue
                old = state.objectives[objective.objective_id]
                state.objectives[objective.objective_id] = min(objective.required, old + amount)
                if state.objectives[objective.objective_id] != old:
                    updates.append(QuestUpdate(quest_id, objective.objective_id))
            if all(state.objectives[obj.objective_id] >= obj.required for obj in quest.objectives):
                state.status = "completed"
                updates.append(QuestUpdate(quest_id, None, completed=True))
                if not state.reward_claimed:
                    state.reward_claimed = True
                    rewards.append((quest_id, quest.rewards))
        for quest_id in self._activate_available():
            updates.append(QuestUpdate(quest_id, None, activated=True))
        return updates, rewards

    def _activate_available(self):
        activated = []
        changed = True
        while changed:
            changed = False
            for quest_id, quest in self.definitions.items():
                state = self.progress[quest_id]
                if state.status == "locked" and all(self.is_completed(key) for key in quest.prerequisites):
                    state.status = "active"
                    activated.append(quest_id)
                    changed = True
        return activated

    def is_completed(self, quest_id):
        return quest_id in self.progress and self.progress[quest_id].status == "completed"

    def active_quests(self):
        return [(q, self.progress[q.quest_id]) for q in self.definitions.values() if self.progress[q.quest_id].status == "active"]

    def visible_quests(self):
        return [(q, self.progress[q.quest_id]) for q in self.definitions.values() if self.progress[q.quest_id].status != "locked"]

    @staticmethod
    def objective_text(objective, state):
        current = state.objectives[objective.objective_id]
        suffix = f" ({current}/{objective.required})" if objective.required > 1 else ""
        return ("Done: " if current >= objective.required else "") + objective.description + suffix

    def to_dict(self):
        """Return JSON-safe state for the Phase 12 save system."""
        return {key: {"status": value.status, "objectives": dict(value.objectives), "reward_claimed": value.reward_claimed} for key, value in self.progress.items()}

    def _load(self, known_npcs, known_areas):
        try:
            raw_quests = json.loads(self.data_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise QuestDataError(f"Could not load {self.data_path.name}: {error}") from error
        if not isinstance(raw_quests, list):
            raise QuestDataError("Quest data must contain a JSON list")
        definitions = {}
        for raw in raw_quests:
            try:
                objectives = tuple(QuestObjective(obj["id"], obj["description"], obj["event"], obj.get("target"), obj.get("required", 1)) for obj in raw["objectives"])
                quest = QuestDefinition(raw["id"], raw["title"], raw["description"], raw["kind"], raw["chapter"], tuple(raw.get("prerequisites", [])), objectives, raw.get("rewards", {}))
            except (KeyError, TypeError) as error:
                raise QuestDataError(f"Invalid quest record: {raw}") from error
            self._validate(quest, known_npcs, known_areas)
            if quest.quest_id in definitions:
                raise QuestDataError(f"Duplicate quest id '{quest.quest_id}'")
            definitions[quest.quest_id] = quest
        for quest in definitions.values():
            if set(quest.prerequisites) - set(definitions) or quest.quest_id in quest.prerequisites:
                raise QuestDataError(f"Quest '{quest.quest_id}' has invalid prerequisites")
        return definitions

    @staticmethod
    def _validate(quest, known_npcs, known_areas):
        if quest.kind not in VALID_KINDS or not quest.objectives:
            raise QuestDataError(f"Quest '{quest.quest_id}' has an invalid kind or no objectives")
        ids = [obj.objective_id for obj in quest.objectives]
        if len(ids) != len(set(ids)):
            raise QuestDataError(f"Quest '{quest.quest_id}' has duplicate objective ids")
        for obj in quest.objectives:
            if obj.event not in VALID_EVENTS or not isinstance(obj.required, int) or obj.required <= 0:
                raise QuestDataError(f"Quest '{quest.quest_id}' has an invalid objective")
            if obj.event in {"talk_to_npc", "defeat_trainer"} and obj.target not in set(known_npcs):
                raise QuestDataError(f"Quest '{quest.quest_id}' references unknown NPC '{obj.target}'")
            if obj.event == "visit_area" and obj.target not in set(known_areas):
                raise QuestDataError(f"Quest '{quest.quest_id}' references unknown area '{obj.target}'")
        rewards = quest.rewards
        if not isinstance(rewards.get("money", 0), int) or rewards.get("money", 0) < 0:
            raise QuestDataError(f"Quest '{quest.quest_id}' has invalid money")
        for item_id, count in rewards.get("items", {}).items():
            if item_id not in ITEM_DATABASE or not isinstance(count, int) or count <= 0:
                raise QuestDataError(f"Quest '{quest.quest_id}' has an invalid item reward")
