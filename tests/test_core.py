"""Fast release regression tests using only the standard unittest runner."""

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
from pathlib import Path

from game.accounts import OfflineAccountProvider
from game.network_protocol import MessageEnvelope, ProtocolError
from game.party import PartyManager
from game.player import Player, PlayerAppearance
from game.pokemon_data import create_pokemon
from game.trading import TradeService
from game.weather import WorldSimulation
from game.region_map import RegionMap
from game.world import WorldManager


class CoreReleaseTests(unittest.TestCase):
    def test_world_cycle(self):
        world = WorldSimulation()
        world.advance_hours(14)
        self.assertEqual(world.time_of_day, "night")
        self.assertEqual(world.clock_text, "22:00")

    def test_player_appearance_has_six_valid_choices(self):
        choices = {PlayerAppearance(gender, skin) for gender in ("male", "female") for skin in range(3)}
        self.assertEqual(len(choices), 6)
        player = Player(appearance=PlayerAppearance("female", 2))
        self.assertEqual((player.appearance.gender, player.appearance.skin), ("female", 2))
        with self.assertRaises(ValueError):
            PlayerAppearance("unknown", 0)

    def test_protocol_round_trip_and_rejection(self):
        identity = OfflineAccountProvider().create_guest("Test")
        message = MessageEnvelope.create("presence", identity.player_id, {"area": "starting_town"})
        self.assertEqual(MessageEnvelope.decode(message.encode()), message)
        with self.assertRaises(ProtocolError):
            MessageEnvelope.create("unknown", identity.player_id, {}).encode()

    def test_atomic_trade(self):
        left_identity = OfflineAccountProvider().create_guest("Left")
        right_identity = OfflineAccountProvider().create_guest("Right")
        left, right = PartyManager(), PartyManager()
        treecko, torchic = create_pokemon("treecko", 5), create_pokemon("torchic", 5)
        left.add_pokemon(treecko); right.add_pokemon(torchic)
        service = TradeService()
        result = service.execute_local(service.create_offer(left_identity, right_identity, treecko, torchic), left, right)
        self.assertTrue(result.success)
        self.assertEqual(left.party[0].pokemon_id, torchic.pokemon_id)

    def test_region_map_references_real_areas_and_hides_secret(self):
        root = Path(__file__).resolve().parent.parent
        world = WorldManager(root / "maps")
        region = RegionMap(root / "maps" / "overviews" / "beta_region.json", world.areas)
        self.assertEqual(set(region.visible_locations(set())), {
            "starting_town", "route_1", "beta_forest", "first_city"
        })
        self.assertIn("starfall_clearing", region.visible_locations({"jirachi_event_unlocked"}))


if __name__ == "__main__":
    unittest.main()
