"""Item and inventory system for Pokemon Beta Blue."""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Item:
    item_id: str
    name: str
    description: str
    category: str
    power: int = 0
    capture_rate: int = 0


ITEM_DATABASE = {
    "poke_ball": Item(item_id="poke_ball", name="Poke Ball", description="A basic catching device.", category="ball", capture_rate=40),
    "great_ball": Item(item_id="great_ball", name="Great Ball", description="A stronger ball for rare Pokemon.", category="ball", capture_rate=60),
    "potion": Item(item_id="potion", name="Potion", description="Restores a small amount of HP.", category="potion", power=20),
}


class Inventory:
    def __init__(self):
        self.items: Dict[str, int] = {"poke_ball": 8, "potion": 3}

    def add(self, item_id: str, count: int = 1):
        self.items[item_id] = self.items.get(item_id, 0) + count

    def remove(self, item_id: str, count: int = 1):
        current = self.items.get(item_id, 0)
        removed = min(current, count)
        if removed > 0:
            self.items[item_id] = current - removed
        return removed

    def count(self, item_id: str):
        return self.items.get(item_id, 0)

    def use_potion(self, pokemon):
        if self.remove("potion", 1):
            heal_amount = ITEM_DATABASE["potion"].power
            pokemon.current_hp = min(pokemon.max_hp, pokemon.current_hp + heal_amount)
            return True
        return False

    def capture_roll(self, ball_id: str, pokemon):
        ball = ITEM_DATABASE.get(ball_id)
        if not ball:
            return False
        base = pokemon.species.catch_rate
        chance = min(95, max(5, base + ball.capture_rate))
        return __import__("random").randint(1, 100) <= chance
