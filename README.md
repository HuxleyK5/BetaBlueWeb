# Pokémon Beta Blue

Pokémon Beta Blue is an expandable, open-world monster-catching RPG built with Python and Pygame. Development is being completed one approved phase at a time so working systems remain stable.

## Completed phases

### Phase 1: Project Foundation

The current modular foundation includes:

- `main.py` — stable project launcher
- `game/main.py` — application lifecycle, state routing, and game loop
- `game/config.py` and `game/settings.json` — code constants plus editable runtime settings
- `game/window.py` — resizable/fullscreen window with aspect-ratio-safe presentation
- `game/input.py` — centralized action bindings and text/movement helpers
- `game/assets.py` — cached image/font loading and missing-asset fallbacks
- top-level content folders for assets, sprites, maps, characters, Pokémon, battles, items, UI, sounds, saves, scripts, and quests

The large `pokemon_game.py` remains intact as the original working prototype. Its mechanics and artwork are reference material for later migration into the modular package.

## Setup and run

Python 3.10 or newer is recommended.

```powershell
python -m pip install -r requirements.txt
python main.py
```

Controls:

- Enter: start/confirm
- Arrow keys or WASD: move
- Q: open/close the quest journal
- I: open/close the Trainer Bag
- N: open/close the Pokémon Nursery
- R: open/close the Beta Region map
- F5: manually save during exploration
- F9: load the current save
- F6: wait six in-game hours during exploration
- M: open the offline multiplayer foundation screen
- F3: toggle performance and asset-cache diagnostics
- F11: toggle fullscreen
- Close the window: quit

### Phase 2: Player System

The modular player now supports eight-direction tile movement, held-key movement, frame-rate-independent speed, animated walking, collision boundaries, diagonal corner protection, trainer statistics, and a smooth camera. The current 40×30 development field is intentionally larger than the screen so camera behavior can be tested before Phase 3 introduces data-driven world maps.

`PlayerStats` owns trainer progression such as money, badges, Pokédex counts, steps, and play time. Keeping these values separate from rendering and movement will make Phase 12 save serialization straightforward.

### Phase 3: Open World Map System

Four connected, data-driven areas now form the first Beta Region path:

`Bluebell Town → Beta Route 1 → Beta Forest → Azure City`

Each JSON file in `maps/` owns its identity, location type, description, spawn point, tile rows, and connections. Maps use a compact tile legend (`.`, `P`, `W`, `T`, `B`, `M`, `G`, and `F`) for grass, paths, water, trees, buildings, mountains, tall grass, and flowers. `WorldManager` validates every map, spawn, transition tile, target area, and destination before play begins.

Crossing a connection keeps the player in the exploration state, safely relocates them inside the adjacent area, rebuilds the bounded camera, and displays a short location banner.

### Phase 4: Pokémon Database System

Pokémon content is now separated from runtime code:

- `Pokemon/data/species.json` stores species identity, types, abilities, all six base stats, level-up learnsets, evolution methods, sprite paths, catch rates, and experience growth groups.
- `Pokemon/data/moves.json` stores reusable move definitions.
- `game/pokemon.py` contains immutable content models and mutable individual Pokémon.
- `game/pokemon_database.py` loads, indexes, and validates content.
- `game/pokemon_data.py` preserves the earlier import interface for battle, encounter, item, and party systems.

The initial dataset contains 19 species covering six complete evolution families plus Jirachi, and 24 moves. Species can be retrieved by stable text key or National Pokédex ID. Individual Pokémon calculate all six stats by level, select an ability, learn up to four eligible moves, gain experience, and stop at level 100.

To add a species, add its record to `species.json`, confirm every move key exists in `moves.json`, add its sprite under `Pokemon/img/`, and ensure every evolution target also exists. Invalid IDs, types, stats, growth groups, learnsets, sprites, or cross-references stop startup with a descriptive error.

### Phase 5: Wild Pokémon System

`Pokemon/data/encounters.json` defines encounter tables independently from maps and species. Each table specifies an area, terrain zone, per-step encounter rate, and weighted entries containing species, level range, rarity, and optional environmental conditions.

Supported zones are tall grass, water, and cave floor. Supported rarity labels are common, uncommon, rare, and legendary. Weather, season, and time-of-day filters are already validated and evaluated through `EncounterContext`; Phase 13 will update that context dynamically.

Only tall grass triggers encounters during normal walking. Water tables are ready for surfing, and wildcard cave tables apply automatically to future cave maps. A four-step grace period after travel or an encounter prevents frustrating immediate repeats. The encounter reveal pauses world movement, loads the selected species sprite, and hands the opponent to the battle system.

### Phase 6: Battle System

Wild encounter reveals now lead into playable turn-based battles. New games include a Treecko, Torchic, or Mudkip selection before exploration. The selected Pokémon is stored in the existing party manager and retains HP, status, moves, PP usage, and experience between battles.

The battle engine is independent from rendering and supports wild, trainer, gym, and boss categories plus single and double formats. It resolves move priority and modified Speed, physical versus special stats, accuracy, STAB, critical hits, random damage variance, all 18 type matchups, dual types, immunity, PP, stat stages, reserve promotion, Struggle, escape rules, fainting, and experience rewards.

Burn, poison, paralysis, and sleep behavior is supported. Current move data can inflict burn and poison, apply stat changes, drain HP, hit twice, or cause recoil. The battle UI displays sprites, levels, HP, status, move type/category, remaining PP, recent feedback, victory or defeat, and XP gained.

### Phase 7: Capture and Storage System

The battle Bag now exposes available Poké Balls. Capture odds use the target's species catch rate, remaining HP, persistent status, ball modifier, type, terrain, time of day, and legendary-event permissions. Each attempt performs four independent shake checks and displays a timed throw-and-shake animation before resolving.

Supported balls are Poké, Great, Ultra, Net, Dusk, and Master Balls. Net Balls receive their bonus against Water or Bug types; Dusk Balls receive theirs at night or in caves. Master Balls guarantee success only after any required legendary-event gate is satisfied.

Captured Pokémon fill the six-member party first, then enter the first available slot across eight named storage boxes of 30 Pokémon each. Party members can be deposited, storage occupants withdrawn, and the active party position remains valid after changes. A throw is blocked without consuming a ball if both party and storage are full.

### Phase 8: NPC and Trainer Systems

NPCs are defined in `characters/npcs.json` and validated against maps, Pokémon, items, patrol points, schedules, shops, and rewards during startup. Runtime NPC state tracks interaction, trainer defeat, one-time reward claims, movement timers, patrol progress, and active schedule blocks.

The first population includes Professor Laurel, a scheduled Bluebell resident, rival Avery, a wandering forest ranger, Azure City's shopkeeper, and Gym Leader Marina. Role colors and `!` markers distinguish their purposes. NPCs occupy collision tiles, face the player during conversations, patrol or wander without entering blocked, transition, NPC, or player tiles, and relocate when schedule periods change.

Enter or Space interacts with the tile the player faces. Dialogue can dispatch into one-time item rewards, trainer/rival/gym battles, or a functional shop. Trainer AI scores move power, STAB, type effectiveness, priority, targets, and difficulty. Winning awards money and, for Marina, the Current Badge. Defeated trainers use post-battle dialogue and cannot be farmed for rewards.

### Phase 9: Story and Quest System

`quests/quests.json` defines main-story, side, Gym, and legendary quests without embedding progression rules in the game loop. Each quest has stable IDs, a chapter, prerequisites, objectives, and rewards. Startup validation rejects broken NPC, area, item, event, objective, and prerequisite references.

Gameplay systems publish semantic events such as choosing a starter, talking to an NPC, visiting an area, defeating a trainer, earning a badge, and catching a species. `QuestManager` turns those events into objective progress, unlocks dependent quests, and grants rewards exactly once. Its runtime state is JSON-safe for Phase 12 saves.

The initial graph includes the three-part Beta Region opening story, the optional Forest Field Notes research quest, Current Badge progression, and the Wish Upon Beta legendary quest. Completing the legendary quest unlocks the starfall conditions required for Jirachi encounters in Beta Forest. `StoryProgress` separately owns chapters, badges, and durable world-event flags.

Press Q during exploration to open the journal. It shows active and completed quests, objective progress, category, description, and rewards. A compact world tracker shows the next objective, while updates and completions appear as timed notices.

### Phase 10: Items and Economy

`items/items.json` is now the authoritative item catalog. It defines names, descriptions, categories, effects, power, capture modifiers, buy prices, sell prices, and whether an item is consumed. Startup validation protects the game from duplicate IDs, invalid prices, unknown categories, and unusable capture balls.

The Trainer Bag separates medicine, Poké Balls, evolution items, and key items into pockets. Press I during exploration to browse it, select usable medicine, and target a party Pokémon. Potions restore HP, Revives restore fainted Pokémon, and status medicine cures persistent conditions. Items are only consumed after a valid use; evolution stones are safely reserved for Phase 11, and key items cannot be used, discarded, or sold.

Shop transactions now run through `ShopService`, keeping money and inventory changes atomic. Azure Supply has a larger catalog and supports Buy and Sell modes. Purchases check funds and the 999-item inventory cap; selling uses catalog prices and removes exactly one item per transaction. Inventory and catalog state are already structured for Phase 12 saving.

### Phase 11: Advanced Pokémon Features

`EvolutionService` evaluates level, friendship, item, trade, and conditional evolution records from the species database. Evolution preserves proportional HP, nickname, friendship, personality, gender, and experience while safely updating species, ability, stats, and available moves. Level and friendship evolution checks run after victories; friendship also grows through travel. Wurmple's personality determines its branch.

The normal starter level evolutions remain available. Beta Region research also provides optional routes that make every evolution method playable now: Treecko can use a Leaf Stone, a highly friendly Torchic can evolve, and Mudkip can use the single-player Link Cable trade substitute. Evolution items are consumed only after a valid evolution.

Press N during exploration to open the Bluebell Pokémon Nursery. Two opposite-gender Pokémon sharing an Egg group can produce an Egg, while genderless and Undiscovered-group Pokémon cannot breed. Eggs track required and completed walking steps independently, may inherit a move known by both parents, and automatically hatch at level 1 into the party or storage when space is available.

Friendship, personality, gender, Egg progress, and Nursery state expose JSON-safe representations for Phase 12. Species records support expandable Egg groups and hatch-step requirements; Jirachi is explicitly in the Undiscovered group.

### Phase 12: Save and Load System

`SaveManager` writes a versioned `saves/savegame.json` containing trainer statistics, exact world position and direction, party and storage, complete individual Pokémon state, inventory, quests, story, NPC state, Nursery Eggs, encounter context, and settings. Temporary battle, dialogue, and shop objects are excluded so loading resumes safely in exploration.

Saving uses a temporary file in the same directory, flushes it to disk, preserves the previous valid save as `savegame.json.bak`, and atomically replaces the primary file. Loading validates and reconstructs the complete candidate state before changing the running game, so corrupt or incompatible files produce a readable error without partially changing a playthrough.

Press F5 during exploration, the Bag, Quest Journal, or Nursery to save manually. Area transitions, completed battles, conversations, and safely dismissed encounters create autosaves. Press F9 to reload, or press C on the title screen when Continue is available. F11 display changes persist to `game/settings.json`; saves also carry a settings snapshot. Save files remain ignored by Git.

### Phase 13: Advanced Open World Features

`WorldSimulation` now advances a real in-game clock at four game minutes per real second. Dawn, day, dusk, and night change automatically; a four-season calendar advances every three in-game days per season. Regional weather changes in deterministic 90–180 minute periods using season-specific probabilities for clear skies, sun, rain, fog, storms, and snow. Press F6 to wait six hours when testing scheduled content.

Exploration is visually affected by seasonal color tint, day/night lighting, rain, storm, fog, snow, and Starfall overlays. The world HUD reports the day, 24-hour time, season, and effective local weather. Timed events are defined and validated in `maps/events/world_events.json`; current examples include the Azure Day Market, Forest Mist, and the legendary Starfall event.

Starfall Clearing is a genuine hidden map rather than a menu destination. After completing Wish Upon Beta, visit Beta Forest at night and find the shimmering path near the eastern clearing. The route remains inaccessible until its story and time conditions are satisfied. Starfall itself occurs there and in Beta Forest only on winter nights after the legendary quest, enabling Jirachi encounters under the same environmental rules used by every wild encounter table.

The save schema is now version 2 and persists the complete world clock, base weather, remaining weather duration, and deterministic seed. Existing Phase 12 version-1 saves migrate automatically, with their former encounter context converted into an equivalent clock and season before play resumes.

### Phase 14: Multiplayer Foundation

Multiplayer is now divided into transport-neutral identity, protocol, trading, and battle-command layers. `AccountProvider` defines future sign-in behavior while `OfflineAccountProvider` supplies a persistent guest identity without credentials or network access. `Transport` defines the future connection boundary; the included `LoopbackTransport` only echoes validated messages in memory and never opens a socket.

Every Pokémon now owns a stable unique ID saved independently from its mutable party or storage position. Trade offers bind both player IDs, both Pokémon IDs, and SHA-256 fingerprints of the offered state. Local execution rechecks ownership and fingerprints before making an atomic exchange; changed, duplicated, missing, or non-pending offers are rejected. The same service boundary can later be hosted by an authoritative server.

Online battle foundations use server-compatible match snapshots, deterministic random seeds, immutable player/team records, and turn-numbered commands. Commands must match the correct match, participant, turn, actor, move, and target before they can enter a future authoritative battle resolver. Existing local battles remain unchanged.

Press M during exploration to inspect player identity, provider, transport, and connection status. Enter toggles the local loopback connection for protocol testing. The game launches and remains fully playable offline. Save schema version 3 persists player and Pokémon ownership identity, and automatically migrates version-1 and version-2 saves with deterministic IDs.

### Phase 15: Polish and Release Preparation

Static map layers are now rendered once and cached instead of rebuilding every visible tile every frame. Starter sprites preload through the centralized asset cache, and F3 displays rolling frame time, estimated FPS, and cache counts. Headless release validation currently starts and validates the complete game in under one second on the development machine.

`AudioManager` supplies short original procedural cues for confirmation, errors, encounters, battles, captures, and quest completion. Cues are cached after first use, obey master/SFX volume settings, and fall back silently when no audio device is available. No external sound library or copyrighted audio asset is required.

Play-time accounting now includes battles and menus. Safe shutdown attempts one final autosave, display/audio preferences reload correctly, the title screen has subtle motion and version labeling, and uncaught launcher failures create `crash.log` in the writable user-data directory. Packaged builds likewise store saves and settings under local application data rather than beside read-only bundled assets.

Release infrastructure includes `scripts/validate_release.py`, standard-library regression tests, `pyproject.toml`, pinned development requirements, a PyInstaller `build.ps1`, [build instructions](BUILDING.md), [release notes](RELEASE_NOTES.md), and a [release checklist](RELEASE_CHECKLIST.md). Public or commercial release remains blocked until Pokémon branding and sprite rights are replaced or legally cleared.

### Beta Region Overview

Press R during exploration to open the illustrated Beta Region map. Its original geography is a presentation asset, while location names, colored markers, white route links, current-position highlighting, and secret-location visibility come from `maps/overviews/beta_region.json`. This separation keeps the map readable and makes later regions straightforward to add without repainting labels into an image.

## Phase 12 test checklist

1. The title screen opens from `python main.py`.
2. Enter opens name entry; typing a name and pressing Enter opens the map.
3. Arrow keys or WASD move in all eight directions; holding keys continues movement.
4. Walking visibly animates and the status bar updates direction and completed steps.
5. Trees, water, and map edges block movement, including diagonal corner cutting.
6. Walk north through Bluebell Town to enter Beta Route 1.
7. Continue north to Beta Forest and then Azure City.
8. Walk south through the same connections to return to Bluebell Town.
9. Confirm each area displays distinct terrain and a location banner.
10. F11 and window resizing continue to work.
11. Run `python main.py`; database validation occurs automatically during startup.
12. Confirm the game starts without a Pokémon data or missing-sprite error.
13. Walk through ordinary grass and paths; neither should trigger encounters.
14. Walk repeatedly through dark tall-grass tiles on Route 1 or in Beta Forest.
15. Confirm a reveal shows species, level, terrain, and rarity, then press Enter to resume.
16. Confirm another encounter cannot occur during the first four eligible steps afterward.
17. Start a new game, select a starter with Left/Right, and confirm with Enter.
18. Trigger a tall-grass encounter and press Enter to battle.
19. Select FIGHT, choose moves with arrows or WASD, and press Enter to execute a round.
20. Verify HP, PP, effectiveness messages, statuses, and XP update correctly.
21. Select RUN in a wild battle and verify escape can succeed or fail.
22. Finish a battle and press Enter to return to the same world position.
23. During a wild battle, select BAG and choose a Poké Ball.
24. Damage or status the wild Pokémon and verify later attempts become more likely to succeed.
25. Watch the throw and shake animation; failed captures allow the opponent to respond.
26. Confirm successful captures join the party and increment the caught statistic.
27. With six party members, confirm the next capture reports that it was sent to Box 1.
28. Face Professor Laurel in Bluebell Town and press Enter; finish the dialogue and confirm two Potions are awarded once.
29. Observe Mira following her patrol without crossing walls or the player.
30. Talk to Avery on Route 1 and verify a trainer battle begins and RUN is rejected.
31. Defeat Avery, talk again, and verify post-battle dialogue appears without another reward.
32. Visit Tess in Azure City, purchase an item, and verify money and inventory update.
33. Defeat Leader Marina and confirm money plus the Current Badge are awarded once.
34. Press Q in the world and verify the journal opens; use Up/Down to browse and Q or Escape to close it.
35. Choose a starter, talk to Professor Laurel, enter Route 1, and defeat Avery; verify A New Journey completes and rewards are added once.
36. Enter Beta Forest, defeat Ranger Rowan, and reach Azure City; verify The Forest Road completes and the Gym quest unlocks.
37. Defeat Leader Marina and verify both Gym objectives complete, the badge count updates, and the next chapter appears.
38. Catch Wurmple and Poochyena in either order; verify Forest Field Notes tracks and completes both objectives.
39. After finishing the Gym and research quests, talk to Laurel and return to Beta Forest; verify Wish Upon Beta completes.
40. Revisit completed objectives and NPCs; confirm quest money and item rewards cannot be claimed twice.
41. Press I during exploration and verify Left/Right changes pockets and Up/Down selects items.
42. Damage a party Pokémon, use a Potion from the Medicine pocket, and verify HP and quantity update once.
43. Try medicine on an invalid target, such as a full-HP Pokémon, and verify the item is not consumed.
44. Cure a status condition with an Antidote or Full Heal and revive a fainted Pokémon with a Revive.
45. Open Azure Supply, purchase several catalog items, and verify money and inventory totals remain synchronized.
46. Switch the shop to Sell mode with Left/Right, sell an item, and verify the displayed sell price is awarded.
47. Confirm key items never appear in the Sell list and evolution stones report that they cannot be used yet.
48. Spend below an item's price and fill an item stack to its cap; verify both invalid purchases are rejected safely.
49. Level Treecko, Torchic, or Mudkip to 16 through battle and verify it evolves after the winning battle.
50. Level Wurmple to 7 and verify its hidden personality consistently selects Silcoon or Cascoon.
51. Buy a Leaf Stone, target Treecko from the Bag, and verify a successful evolution consumes exactly one stone.
52. Try the same stone on an incompatible Pokémon and verify no item is consumed.
53. Raise Torchic's friendship through victories and travel, then verify its friendship evolution at the configured threshold.
54. Buy a Link Cable and use it on Mudkip; verify the single-player trade evolution works without disabling normal level evolution.
55. Press N with two compatible, opposite-gender Pokémon and create an Egg; verify incompatible pairs are rejected.
56. Walk until the Nursery Egg reaches zero remaining steps and verify it hatches at level 1 into the party or storage.
57. Breed parents sharing a known move and verify the hatchling can inherit that move while retaining a four-move limit.
58. Confirm Jirachi and genderless or Undiscovered-group Pokémon cannot breed.
59. Press F5 during exploration and confirm the save notice appears and `saves/savegame.json` is created.
60. Change areas, spend money, damage a Pokémon, progress a quest, and create an Egg; save, alter those values, then press F9 and verify all values return.
61. Restart the game, press C on the title screen, and verify the trainer resumes at the saved area and tile.
62. Confirm party order, active member, fainted HP, friendship, personality, gender, known moves, and storage occupants survive a restart.
63. Confirm inventory, money, badges, story, quest objectives, NPC reward states, and Egg steps survive a restart.
64. Complete a battle or cross a connection, restart, and verify the autosave captured the safe post-event state.
65. Save twice and confirm `savegame.json.bak` exists beside the primary save.
66. Corrupt a copied save and verify loading reports an error without changing the running playthrough.
67. Press F5 during a battle and verify saving is refused instead of recording unstable mid-battle state.
68. Toggle fullscreen with F11, restart, and verify the display preference persists.
69. Watch the HUD clock pass through dawn, day, dusk, and night; verify the lighting changes without changing maps.
70. Press F6 repeatedly and verify time advances six hours while days and seasons roll forward correctly.
71. Observe at least two weather changes and verify rain, fog, storms, or snow use the correct visual overlay.
72. Visit Azure City during clear or sunny daytime and verify the Azure Day Market event label appears.
73. Visit Beta Forest during foggy dawn and verify the Forest Mist event becomes active.
74. Before completing Wish Upon Beta, visit tile 22,15 in Beta Forest at night and confirm no hidden path opens.
75. Complete Wish Upon Beta, return at night, follow the eastern shimmer, and verify entry into Starfall Clearing.
76. Leave Starfall Clearing through its southern path and verify return to the same Beta Forest clearing.
77. Reach a winter night after the legendary quest and verify Starfall overrides local weather in the forest and clearing.
78. Walk through Starfall Clearing grass and verify Jirachi is eligible only during the complete legendary event conditions.
79. Save during one season and weather period, reload, and verify time, weather, and remaining duration are unchanged.
80. Load a Phase 12 schema-version-1 save copy and verify it migrates and resumes without losing progression.
81. Press M during exploration and verify the multiplayer foundation screen displays the offline guest identity.
82. Press Enter on that screen and confirm the loopback state changes to Connected without requiring internet access.
83. Press Enter again and confirm it returns to Offline while single-player progress remains unchanged.
84. Save, restart, and verify the player ID and every party/storage Pokémon ID remain unchanged.
85. Load a copied schema-version-2 save and verify deterministic identity migration preserves all previous progression.
86. Create a local trade offer, change the offered Pokémon's HP, and verify fingerprint validation rejects the exchange.
87. Complete a valid local trade test and verify both Pokémon exchange atomically with their IDs intact.
88. Duplicate a Pokémon ID in a copied save and verify loading rejects it without partially changing the running game.
89. Create a deterministic online match snapshot and verify commands from the wrong player, match, or turn are rejected.
90. Disconnect loopback, restart, and verify wild battles, trainer battles, captures, saves, and quests still work offline.
91. Press F3 and verify frame time, FPS, cached-image count, and cached-font count appear without pausing play.
92. Enter every map and verify its static layer renders correctly while movement, NPCs, weather, and secret markers remain dynamic.
93. Trigger confirmation, error, encounter, battle, capture, and quest cues; verify volume settings apply consistently.
94. Run without an available audio device and verify the game remains fully playable without audio errors.
95. Spend time in battles, the Bag, Quest Journal, Nursery, and multiplayer screen; verify play time continues increasing.
96. Close the window during safe exploration, restart, and verify the final shutdown autosave can be continued.
97. Run `python scripts/validate_release.py` and the unittest command from `BUILDING.md`; verify both pass.
98. Build with `build.ps1`, move the complete output folder to a clean machine, and verify all bundled data loads.
99. Intentionally test an uncaught startup failure in a disposable copy and verify a readable `crash.log` is created.
100. Complete every automated, gameplay, presentation, packaging, and legal gate in `RELEASE_CHECKLIST.md` before distribution.

## Architecture direction

Runtime systems live under `game/`; content belongs in the matching top-level folder. Configuration, input, window presentation, and assets are centralized so later regions and game modes do not duplicate platform code.

The planned Phase 1–15 architecture pass is complete. Future work should proceed as versioned milestones driven by playtesting, original content production, accessibility, balance, and legally cleared release assets rather than adding unbounded systems to the core loop.
