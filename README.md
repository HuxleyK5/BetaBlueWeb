# Pokémon Beta Blue

## Phase 1 Foundation
This repository now contains a modular game package under `game/`.

### What was added
- `game/config.py` — configuration constants and game state IDs
- `game/input.py` — input handling and movement sanitization
- `game/assets.py` — lightweight asset loading and folder initialization
- `game/window.py` — window setup, fullscreen toggle, and screen scaling
- `game/player.py` — player movement state, smooth tile movement, and simple rendering
- `game/map.py` — tile-based map definitions, collision rules, and rendering
- `game/main.py` — entry point and game loop with title/name/town states

### Testing Phase 1
1. Install Pygame if needed: `pip install pygame`
2. Run the game: `python game/main.py`
3. Verify:
   - Title screen appears
   - ENTER goes to name entry
   - typing name and ENTER enters the town
   - arrow keys move the player on a tile map
   - player cannot walk through trees or water

### Next phase
Phase 2 will add the player character system, 8-direction movement, animations, collision handling, and camera following. It will also begin replacing the prototype map logic with a world-focused map scene.
