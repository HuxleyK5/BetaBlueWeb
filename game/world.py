"""World and region management for Pokemon Beta Blue."""

from .map import GameMap, TILE_GRASS, TILE_PATH, TILE_WATER, TILE_TREE, TILE_BUILDING, TILE_TALL_GRASS
from .npc import NPC
from .pokemon_data import create_pokemon


class Area(GameMap):
    def __init__(self, name, description, tile_map, transitions=None, npcs=None):
        super().__init__(tile_map)
        self.name = name
        self.description = description
        self.transitions = transitions or {}
        self.npcs = npcs or []

    def get_transition(self, x, y):
        return self.transitions.get((x, y))


class WorldManager:
    def __init__(self):
        self.areas = {}
        self.current_area = None
        self.load_world()

    def load_world(self):
        self.areas["starting_town"] = Area(
            name="Starting Town",
            description="A quiet village with an open path to the wild.",
            tile_map=[
                [TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_PATH, TILE_PATH, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_PATH, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_TREE, TILE_BUILDING, TILE_BUILDING, TILE_BUILDING, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_TREE, TILE_BUILDING, TILE_BUILDING, TILE_BUILDING, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_TREE, TILE_BUILDING, TILE_BUILDING, TILE_BUILDING, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH],
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_PATH] * 20,
            ],
            transitions={(10, 14): ("route_1", (10, 0))},
            npcs=[
                NPC("Prof. Laurel", 5, 2, ["Welcome to Beta Region.", "Choose a starter and begin your journey!"], is_trainer=False),
            ],
        )
        self.areas["route_1"] = Area(
            name="Route 1",
            description="A grassy path that leads north.",
            tile_map=[
                [TILE_PATH] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS],
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_GRASS] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH],
            ],
            transitions={(10, 0): ("forest", (10, 14)), (10, 14): ("starting_town", (10, 0))},
            npcs=[
                NPC("Bug Catcher", 6, 3, ["My Pokemon are ready.", "Prepare for a quick battle!"], is_trainer=True, party=[create_pokemon("treecko", 6)]),
            ],
        )
        self.areas["forest"] = Area(
            name="Emerald Forest",
            description="A misty woodland full of tall grass and hidden trails.",
            tile_map=[
                [TILE_TREE] * 20,
                [TILE_TREE, TILE_PATH, TILE_PATH, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_WATER, TILE_WATER, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_WATER, TILE_WATER, TILE_TALL_GRASS, TILE_TALL_GRASS, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_TREE, TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] + [TILE_GRASS] * 18 + [TILE_TREE],
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_TREE] * 20,
                [TILE_PATH] * 20,
                [TILE_PATH] * 20,
            ],
            transitions={(10, 14): ("first_city", (10, 0)), (10, 0): ("route_1", (10, 14))},
            npcs=[
                NPC("Ranger", 8, 4, ["Stay on the path in tall grass.", "Wild Pokemon are more common here."], is_trainer=False),
            ],
        )
        self.areas["first_city"] = Area(
            name="Petal City",
            description="A bustling first city with a shop and town square.",
            tile_map=[
                [TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_BUILDING, TILE_BUILDING, TILE_BUILDING, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_BUILDING, TILE_BUILDING, TILE_BUILDING, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE],
                [TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_GRASS, TILE_GRASS, TILE_GRASS, TILE_PATH, TILE_TREE, TILE_TREE, TILE_TREE, TILE_TREE],
                [TILE_PATH] * 20,
            ] + [[TILE_GRASS] * 20 for _ in range(10)],
            transitions={(10, 0): ("forest", (10, 14))},
            npcs=[
                NPC("Shopkeeper", 4, 2, ["Welcome to my shop!", "Press B to buy items later."], is_trainer=False),
            ],
        )
        self.current_area = self.areas["starting_town"]

    def travel_to(self, area_name, destination_tile):
        if area_name not in self.areas:
            return
        self.current_area = self.areas[area_name]
        return destination_tile
