"""Simple Pokedex system for discovery and encyclopedia entries."""

from typing import Set


class Pokedex:
    def __init__(self):
        self.discovered: Set[str] = set()

    def register(self, species_key: str):
        self.discovered.add(species_key.lower())

    def discovered_species(self):
        return sorted(self.discovered)

    def has_discovered(self, species_key: str):
        return species_key.lower() in self.discovered
