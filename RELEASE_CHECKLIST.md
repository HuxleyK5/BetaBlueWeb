# Release Checklist

## Automated gates

- [ ] `python scripts/validate_release.py` passes.
- [ ] `python -m unittest discover -s tests -p "test_*.py"` passes.
- [ ] `python -m compileall -q game main.py` passes.
- [ ] `git diff --check` reports no whitespace errors.
- [ ] F3 diagnostics remain near the target 60 FPS on the minimum test machine.

## Gameplay regression

- [ ] New Game and Continue both reach stable exploration.
- [ ] All maps and bidirectional connections load.
- [ ] Movement, collision, NPCs, shops, quests, battles, captures, evolution, breeding, and hatching work.
- [ ] Day/night, seasons, weather, events, secret paths, and legendary gates work.
- [ ] Manual save, autosave, backup, migration, and corrupt-save rejection work.
- [ ] Offline multiplayer status, loopback, trade validation, and single-player isolation work.

## Presentation and accessibility

- [ ] UI text fits at 800×600 and after window scaling.
- [ ] Keyboard hints match actual controls.
- [ ] Missing audio hardware falls back silently.
- [ ] Master and SFX volume values remain between 0 and 1.
- [ ] Weather overlays preserve sufficient text and character contrast.

## Packaging

- [ ] Build succeeds using `build.ps1` on a clean checkout.
- [ ] The packaged executable finds every JSON, map, sprite, and settings file.
- [ ] A clean machine can launch without Python installed.
- [ ] Saves are written outside bundled read-only assets and survive restart.
- [ ] `crash.log` is generated for an intentionally tested uncaught failure.

## Release blockers

- [ ] Pokémon trademarks, names, and visual assets have been replaced or legally cleared.
- [ ] Third-party asset sources and licenses are documented.
- [ ] Version number and release notes are finalized.
- [ ] No real multiplayer endpoint is advertised; Phase 14 is a local foundation only.
