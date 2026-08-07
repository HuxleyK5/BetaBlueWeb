"""Turn-based battle system for Pokemon Beta Blue."""

import random
from dataclasses import dataclass
from typing import Optional

from .pokemon_data import Pokemon
from .items import Inventory
from .ui import draw_health_bar


TYPE_EFFECTIVENESS = {
    ("Fire", "Grass"): 2.0,
    ("Water", "Fire"): 2.0,
    ("Grass", "Water"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Water", "Grass"): 0.5,
    ("Grass", "Fire"): 0.5,
}


@dataclass
class BattleResult:
    winner: str
    xp_awarded: int = 0
    captured: bool = False


def effectiveness(move_type: str, target_types: list):
    multiplier = 1.0
    for t in target_types:
        multiplier *= TYPE_EFFECTIVENESS.get((move_type, t), 1.0)
    return multiplier


def calculate_damage(attacker: Pokemon, defender: Pokemon, move):
    move_power = move.power
    attack = attacker.attack
    defense = defender.defense
    base = (((2 * attacker.level / 5 + 2) * move_power * attack / defense) / 50) + 2
    multiplier = effectiveness(move.type_name, defender.species.types)
    if random.random() > move.accuracy / 100:
        return 0, 1.0
    raw = int(base * multiplier)
    return max(1, raw), multiplier


class Battle:
    def __init__(self, player_pokemon: Pokemon, enemy_pokemon: Pokemon, inventory: Inventory):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.inventory = inventory
        self.battle_log = []
        self.selected_move_index = 0
        self.turn_owner = "player"
        self.result: Optional[BattleResult] = None

    def select_move(self, index: int):
        if 0 <= index < len(self.player_pokemon.species.moves):
            self.selected_move_index = index

    def player_attack(self):
        move = self.player_pokemon.species.moves[self.selected_move_index]
        damage, multiplier = calculate_damage(self.player_pokemon, self.enemy_pokemon, move)
        if damage == 0:
            self.battle_log.append(f"{self.player_pokemon.species.name}'s {move.name} missed!")
        else:
            self.enemy_pokemon.current_hp -= damage
            effectiveness_text = ""
            if multiplier > 1.5:
                effectiveness_text = " It's super effective!"
            elif multiplier < 1.0:
                effectiveness_text = " It's not very effective..."
            self.battle_log.append(f"{self.player_pokemon.species.name} used {move.name}!{effectiveness_text}")
        self.turn_owner = "enemy"
        self.resolve_turn()

    def enemy_attack(self):
        move = self.enemy_pokemon.species.moves[0]
        damage, multiplier = calculate_damage(self.enemy_pokemon, self.player_pokemon, move)
        if damage == 0:
            self.battle_log.append(f"{self.enemy_pokemon.species.name}'s {move.name} missed!")
        else:
            self.player_pokemon.current_hp -= damage
            self.battle_log.append(f"{self.enemy_pokemon.species.name} used {move.name}!")
        self.turn_owner = "player"
        self.resolve_turn()

    def resolve_turn(self):
        if self.player_pokemon.current_hp <= 0:
            self.player_pokemon.current_hp = 0
            self.result = BattleResult(winner="enemy", xp_awarded=0)
            self.battle_log.append(f"{self.player_pokemon.species.name} fainted!")
        elif self.enemy_pokemon.current_hp <= 0:
            xp = int(self.enemy_pokemon.level * 12)
            self.enemy_pokemon.current_hp = 0
            self.result = BattleResult(winner="player", xp_awarded=xp)
            self.battle_log.append(f"{self.enemy_pokemon.species.name} fainted!")

    def use_item(self, item_id: str):
        if item_id == "potion":
            if self.inventory.use_potion(self.player_pokemon):
                self.battle_log.append("Used Potion. HP restored.")
                self.turn_owner = "enemy"
                self.resolve_turn()
                return True
        elif item_id in ("poke_ball", "great_ball"):
            if self.inventory.capture_roll(item_id, self.enemy_pokemon):
                self.result = BattleResult(winner="player", xp_awarded=0, captured=True)
                self.battle_log.append(f"Captured {self.enemy_pokemon.species.name}!")
            else:
                self.battle_log.append("The Pokemon broke free!")
                self.turn_owner = "enemy"
                self.resolve_turn()
            return True
        return False

    def draw_battle(self, surface, font):
        surface.fill((12, 20, 40))
        draw_health_bar(surface, 40, 80, 260, 24, self.enemy_pokemon.current_hp, self.enemy_pokemon.max_hp)
        draw_health_bar(surface, 40, 320, 260, 24, self.player_pokemon.current_hp, self.player_pokemon.max_hp)
        surface.blit(font.render(self.enemy_pokemon.species.name, True, (255, 255, 255)), (40, 40))
        surface.blit(font.render(self.player_pokemon.species.name, True, (255, 255, 255)), (40, 280))
        log_y = 380
        for line in self.battle_log[-4:]:
            surface.blit(font.render(line, True, (240, 240, 240)), (40, log_y))
            log_y += 28
