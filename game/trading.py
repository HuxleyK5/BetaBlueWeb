"""Ownership-safe trade offers and atomic local exchange."""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import uuid


@dataclass(frozen=True)
class TradeOffer:
    offer_id: str
    sender_id: str
    recipient_id: str
    offered_pokemon_id: str
    requested_pokemon_id: str
    offered_fingerprint: str
    requested_fingerprint: str
    created_at: str
    status: str = "pending"

    def to_dict(self):
        return self.__dict__.copy()


@dataclass(frozen=True)
class TradeResult:
    success: bool
    message: str


class TradeService:
    def create_offer(self, sender, recipient, offered, requested):
        if sender.player_id == recipient.player_id or offered.pokemon_id == requested.pokemon_id:
            raise ValueError("A trade requires two different players and Pokemon")
        return TradeOffer(uuid.uuid4().hex, sender.player_id, recipient.player_id, offered.pokemon_id, requested.pokemon_id, pokemon_fingerprint(offered), pokemon_fingerprint(requested), datetime.now(timezone.utc).isoformat())

    def execute_local(self, offer, sender_party, recipient_party):
        if offer.status != "pending":
            return TradeResult(False, "This trade offer is no longer pending.")
        offered_location = _find(sender_party, offer.offered_pokemon_id)
        requested_location = _find(recipient_party, offer.requested_pokemon_id)
        if offered_location is None or requested_location is None:
            return TradeResult(False, "Trade ownership changed before confirmation.")
        offered = _remove(sender_party, offered_location)
        requested = _remove(recipient_party, requested_location)
        if pokemon_fingerprint(offered) != offer.offered_fingerprint or pokemon_fingerprint(requested) != offer.requested_fingerprint:
            _restore(sender_party, offered, offered_location); _restore(recipient_party, requested, requested_location)
            return TradeResult(False, "Trade Pokemon changed after the offer was created.")
        sender_party.add_pokemon(requested)
        recipient_party.add_pokemon(offered)
        sender_party.active_index = min(sender_party.active_index, len(sender_party.party) - 1)
        recipient_party.active_index = min(recipient_party.active_index, len(recipient_party.party) - 1)
        return TradeResult(True, f"Traded {offered.display_name} for {requested.display_name}.")


def pokemon_fingerprint(pokemon):
    payload = json.dumps(pokemon.to_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _find(manager, pokemon_id):
    for index, pokemon in enumerate(manager.party):
        if pokemon.pokemon_id == pokemon_id:
            return "party", index
    for box_index, box in enumerate(manager.storage.boxes):
        for slot_index, pokemon in enumerate(box.pokemon):
            if pokemon.pokemon_id == pokemon_id:
                return "storage", box_index, slot_index
    return None


def _remove(manager, location):
    if location[0] == "party":
        return manager.party.pop(location[1])
    return manager.storage.boxes[location[1]].pokemon.pop(location[2])


def _restore(manager, pokemon, location):
    if location[0] == "party":
        manager.party.insert(location[1], pokemon)
    else:
        manager.storage.boxes[location[1]].pokemon.insert(location[2], pokemon)
