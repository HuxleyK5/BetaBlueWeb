"""Run deterministic content and headless startup checks before packaging."""

import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from game.main import Game
from game.items import ITEM_DATABASE
from game.pokemon_data import DATABASE


def main():
    started = time.perf_counter()
    game = Game()
    checks = {
        "species": len(DATABASE.species), "moves": len(DATABASE.moves),
        "items": len(ITEM_DATABASE), "maps": len(game.world.areas),
        "npcs": len(game.npcs.npcs), "quests": len(game.quests.definitions),
        "events": len(game.world_events.events),
    }
    assert checks["species"] >= 19 and checks["maps"] >= 5
    assert game.party.has_capture_capacity()
    for area in game.world.areas.values():
        area.game_map.draw(game.window.screen)
    game.draw_title_screen()
    game.performance.draw(game.window.screen, game.small_font, game.assets)
    pygame.quit()
    elapsed = time.perf_counter() - started
    print("Release validation passed")
    print("  " + "  ".join(f"{name}={value}" for name, value in checks.items()))
    print(f"  headless_startup={elapsed:.3f}s  cached_images={game.assets.cache_stats()['images']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
