"""Validated item catalog, inventory pockets, and item effects."""

from dataclasses import dataclass
import json
from pathlib import Path

from .config import PROJECT_ROOT

ITEM_CATEGORIES = ("medicine", "ball", "evolution", "key")


class ItemDataError(ValueError):
    """Raised when item content is malformed."""


@dataclass(frozen=True)
class Item:
    item_id: str
    name: str
    description: str
    category: str
    buy_price: int
    sell_price: int
    effect: str = "none"
    power: int = 0
    ball_modifier: float = 0.0
    consumable: bool = True

    @property
    def usable(self):
        return self.effect in {"heal", "revive", "cure_status", "full_heal", "evolution"}

    @property
    def sellable(self):
        return self.category != "key" and self.sell_price > 0


@dataclass(frozen=True)
class ItemUseResult:
    success: bool
    message: str


def load_item_database(path=None):
    path = Path(path or PROJECT_ROOT / "items" / "items.json")
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ItemDataError(f"Could not load {path.name}: {error}") from error
    if not isinstance(records, list):
        raise ItemDataError("Item data must contain a JSON list")
    database = {}
    for raw in records:
        try:
            item = Item(raw["id"], raw["name"], raw["description"], raw["category"], raw["buy_price"], raw["sell_price"], raw.get("effect", "none"), raw.get("power", 0), raw.get("ball_modifier", 0.0), raw.get("consumable", True))
        except (KeyError, TypeError) as error:
            raise ItemDataError(f"Invalid item record: {raw}") from error
        if item.item_id in database or item.category not in ITEM_CATEGORIES:
            raise ItemDataError(f"Duplicate item or invalid category for '{item.item_id}'")
        numeric = (item.buy_price, item.sell_price, item.power)
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in numeric):
            raise ItemDataError(f"Item '{item.item_id}' has invalid numeric values")
        if not isinstance(item.ball_modifier, (int, float)) or item.ball_modifier < 0:
            raise ItemDataError(f"Item '{item.item_id}' has an invalid ball modifier")
        if item.category == "ball" and item.ball_modifier <= 0:
            raise ItemDataError(f"Ball '{item.item_id}' needs a capture modifier")
        database[item.item_id] = item
    return database


ITEM_DATABASE = load_item_database()


class Inventory:
    MAX_PER_ITEM = 999

    def __init__(self, starting_items=None):
        self.items = {}
        defaults = {"poke_ball": 8, "great_ball": 2, "ultra_ball": 1, "net_ball": 1, "dusk_ball": 1, "potion": 3} if starting_items is None else starting_items
        for item_id, count in defaults.items():
            self.add(item_id, count)

    def add(self, item_id, count=1):
        self._require_item(item_id)
        if not isinstance(count, int) or count <= 0:
            return 0
        added = min(self.MAX_PER_ITEM - self.count(item_id), count)
        if added:
            self.items[item_id] = self.count(item_id) + added
        return added

    def remove(self, item_id, count=1):
        self._require_item(item_id)
        if not isinstance(count, int) or count <= 0:
            return 0
        removed = min(self.count(item_id), count)
        if removed:
            remaining = self.count(item_id) - removed
            if remaining:
                self.items[item_id] = remaining
            else:
                self.items.pop(item_id, None)
        return removed

    def count(self, item_id):
        return self.items.get(item_id, 0)

    def pocket(self, category, sellable_only=False):
        return [item_id for item_id in ITEM_DATABASE if self.count(item_id) and ITEM_DATABASE[item_id].category == category and (not sellable_only or ITEM_DATABASE[item_id].sellable)]

    def pocket_items_for_sale(self):
        return [item_id for category in ITEM_CATEGORIES for item_id in self.pocket(category, sellable_only=True)]

    def use(self, item_id, pokemon):
        self._require_item(item_id)
        item = ITEM_DATABASE[item_id]
        if self.count(item_id) <= 0:
            return ItemUseResult(False, f"You have no {item.name}s.")
        if not item.usable:
            return ItemUseResult(False, f"{item.name} cannot be used right now.")
        if item.effect == "evolution":
            return ItemUseResult(False, "Evolution items are handled by the evolution service.")
        if item.effect == "heal":
            if pokemon.current_hp <= 0:
                return ItemUseResult(False, "A fainted Pokemon needs a Revive.")
            if pokemon.current_hp >= pokemon.max_hp:
                return ItemUseResult(False, f"{pokemon.display_name} already has full HP.")
            restored = min(item.power, pokemon.max_hp - pokemon.current_hp)
            pokemon.current_hp += restored
            message = f"{pokemon.display_name} recovered {restored} HP."
        elif item.effect == "revive":
            if pokemon.current_hp > 0:
                return ItemUseResult(False, f"{pokemon.display_name} has not fainted.")
            pokemon.current_hp = max(1, pokemon.max_hp * item.power // 100)
            message = f"{pokemon.display_name} was revived!"
        else:
            if pokemon.status == "healthy":
                return ItemUseResult(False, f"{pokemon.display_name} has no status condition.")
            old_status = pokemon.status
            pokemon.status = "healthy"
            message = f"{pokemon.display_name} recovered from {old_status}."
        if item.consumable:
            self.remove(item_id)
        return ItemUseResult(True, message)

    def use_potion(self, pokemon):
        return self.use("potion", pokemon).success

    def to_dict(self):
        return dict(self.items)

    @staticmethod
    def _require_item(item_id):
        if item_id not in ITEM_DATABASE:
            raise KeyError(f"Unknown item '{item_id}'")

    def capture_roll(self, ball_id, pokemon):
        """Compatibility wrapper; battle capture uses CaptureCalculator."""
        from .capture import CaptureCalculator
        ball = ITEM_DATABASE.get(ball_id)
        return bool(ball and ball.category == "ball" and CaptureCalculator().attempt(pokemon, ball).success)
