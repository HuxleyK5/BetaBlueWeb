"""Money-safe shop transactions, independent from shop rendering."""

from dataclasses import dataclass
from .items import ITEM_DATABASE


@dataclass(frozen=True)
class TransactionResult:
    success: bool
    message: str
    money_changed: int = 0


class ShopService:
    def buy(self, player_stats, inventory, offer, quantity=1):
        item_id, price = offer["item"], offer["price"]
        item = ITEM_DATABASE[item_id]
        total = price * quantity
        if quantity <= 0:
            return TransactionResult(False, "Choose a valid quantity.")
        if player_stats.money < total:
            return TransactionResult(False, "You don't have enough money.")
        if inventory.count(item_id) + quantity > inventory.MAX_PER_ITEM:
            return TransactionResult(False, f"Your {item.name} pocket is full.")
        player_stats.money -= total
        inventory.add(item_id, quantity)
        return TransactionResult(True, f"Purchased {quantity} {item.name}!", -total)

    def sell(self, player_stats, inventory, item_id, quantity=1):
        item = ITEM_DATABASE[item_id]
        if not item.sellable:
            return TransactionResult(False, f"{item.name} cannot be sold.")
        if quantity <= 0 or inventory.count(item_id) < quantity:
            return TransactionResult(False, "You do not have enough to sell.")
        total = item.sell_price * quantity
        inventory.remove(item_id, quantity)
        player_stats.money += total
        return TransactionResult(True, f"Sold {quantity} {item.name} for ${total:,}.", total)
