$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

python scripts/validate_release.py
python -m unittest discover -s tests -p "test_*.py"
python -m PyInstaller --noconfirm --clean --onedir --name PokemonBetaBlue `
  --add-data "game/settings.json;game" `
  --add-data "maps;maps" `
  --add-data "Pokemon/data;Pokemon/data" `
  --add-data "Pokemon/img;Pokemon/img" `
  --add-data "characters;characters" `
  --add-data "items;items" `
  --add-data "quests;quests" `
  main.py

Write-Host "Build complete: dist/PokemonBetaBlue/PokemonBetaBlue.exe"
