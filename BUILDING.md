# Building Pokémon Beta Blue

## Development run

Use Python 3.10 or newer from the project root:

```powershell
python -m pip install -r requirements.txt
python scripts/validate_release.py
python -m unittest discover -s tests -p "test_*.py"
python main.py
```

The validator uses SDL's dummy video and audio drivers, so it can run on a CI machine without opening a window.

## Windows distributable

Install development tools and invoke the checked-in build script:

```powershell
python -m pip install -r requirements-dev.txt
powershell -ExecutionPolicy Bypass -File build.ps1
```

The script validates content, runs regression tests, and creates an isolated application under `dist/PokemonBetaBlue/`. Test the executable from that directory before distributing it. Build outputs, saves, logs, and generated spec files are ignored by Git.

## Clean-machine verification

Copy the entire `dist/PokemonBetaBlue/` directory to a clean Windows machine. Verify launch, new game, Continue, audio fallback, resizing, fullscreen, saving, all maps, battles, and shutdown. Do not test only from the developer machine, because local Python packages can hide missing bundled data.

## Distribution rights

This repository uses Pokémon names and an existing sprite library. Those assets and trademarks are not automatically cleared for public or commercial distribution. Complete a rights review and replace or license protected names, artwork, sounds, and branding before release. This is a release blocker, not an optional checklist item.
