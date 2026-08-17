"""UI-independent turn-based battle engine for all battle categories."""

from dataclasses import dataclass
from enum import Enum
import random

from .pokemon import Move, Pokemon
from .type_chart import effectiveness


STRUGGLE = Move("struggle", "Struggle", "Normal", "physical", 50, 100, 1, effect="recoil_quarter")


class BattleKind(str, Enum):
    WILD = "wild"
    TRAINER = "trainer"
    GYM = "gym"
    BOSS = "boss"


class BattleFormat(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"


@dataclass(frozen=True)
class BattleAction:
    side: str
    actor_index: int
    move_index: int
    target_index: int = 0


@dataclass(frozen=True)
class BattleResult:
    winner: str
    xp_awarded: int = 0
    levels_gained: int = 0
    escaped: bool = False
    captured: bool = False


def calculate_damage(attacker, defender, move, rng=None, attack_stage=0, defense_stage=0):
    """Return damage and type multiplier using the standard battle components."""
    if move.category == "status" or move.power == 0:
        return 0, effectiveness(move.type_name, defender.species.types)
    rng = rng or random
    attack_stat = attacker.attack if move.category == "physical" else attacker.special_attack
    defense_stat = defender.defense if move.category == "physical" else defender.special_defense
    attack_stat *= _stage_multiplier(attack_stage)
    defense_stat *= _stage_multiplier(defense_stage)
    base = (((2 * attacker.level / 5 + 2) * move.power * attack_stat / max(1, defense_stat)) / 50) + 2
    type_multiplier = effectiveness(move.type_name, defender.species.types)
    stab = 1.5 if move.type_name in attacker.species.types else 1.0
    critical_chance = 1 / 8 if move.effect == "high_critical" else 1 / 24
    critical = 1.5 if rng.random() < critical_chance else 1.0
    variance = rng.uniform(0.85, 1.0)
    burn = 0.5 if attacker.status == "burn" and move.category == "physical" else 1.0
    damage = int(base * type_multiplier * stab * critical * variance * burn)
    return (0 if type_multiplier == 0 else max(1, damage)), type_multiplier


def _stage_multiplier(stage):
    stage = max(-6, min(6, stage))
    return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)


class Battle:
    """Resolve rounds for single or double wild/trainer-style battles."""

    def __init__(self, player_team, enemy_team, kind=BattleKind.WILD, battle_format=BattleFormat.SINGLE, rng=None, enemy_ai=None):
        self.player_team = list(player_team) if isinstance(player_team, (list, tuple)) else [player_team]
        self.enemy_team = list(enemy_team) if isinstance(enemy_team, (list, tuple)) else [enemy_team]
        if not self.player_team or not self.enemy_team:
            raise ValueError("Both battle teams require at least one Pokemon")
        self.kind = BattleKind(kind)
        self.battle_format = BattleFormat(battle_format)
        self.active_count = 2 if self.battle_format == BattleFormat.DOUBLE else 1
        self.rng = rng or random.Random()
        self.enemy_ai = enemy_ai
        self.log = [self._opening_message()]
        self.result = None
        self.turn_number = 1
        self.stat_stages = {
            id(pokemon): {name: 0 for name in ("attack", "defense", "special_attack", "special_defense", "speed", "accuracy")}
            for pokemon in self.player_team + self.enemy_team
        }
        self.pp = {
            (id(pokemon), move.key): move.pp
            for pokemon in self.player_team + self.enemy_team
            for move in pokemon.known_moves
        }
        self.volatile = {id(pokemon): {} for pokemon in self.player_team + self.enemy_team}

    @property
    def player_pokemon(self):
        return self.player_team[0]

    @property
    def enemy_pokemon(self):
        return self.enemy_team[0]

    @property
    def battle_log(self):
        return self.log

    def active_team(self, side):
        team = self.player_team if side == "player" else self.enemy_team
        return [pokemon for pokemon in team[:self.active_count] if pokemon.current_hp > 0]

    def _active_slots(self, side):
        team = self.player_team if side == "player" else self.enemy_team
        return team[:self.active_count]

    def remaining_pp(self, pokemon, move):
        return self.pp.get((id(pokemon), move.key), 0)

    def execute_round(self, player_actions):
        if self.result is not None:
            return self.result
        actions = [action for action in player_actions if self._valid_action(action)]
        actions.extend(self._enemy_actions())
        actions.sort(key=self._action_order, reverse=True)
        for action in actions:
            if self.result is not None:
                break
            self._execute_action(action)
            self._check_finished()
        if self.result is None:
            self._apply_end_turn_statuses()
            self._check_finished()
        if self.result is None:
            self._promote_reserves()
        self.turn_number += 1
        return self.result

    def attempt_escape(self):
        if self.kind != BattleKind.WILD:
            self.log.append("You cannot run from this battle!")
            return False
        player_speed = max(p.speed for p in self.active_team("player"))
        enemy_speed = max(p.speed for p in self.active_team("enemy"))
        chance = min(0.95, max(0.35, 0.5 + (player_speed - enemy_speed) / 200))
        if self.rng.random() < chance:
            self.result = BattleResult("escaped", escaped=True)
            self.log.append("You got away safely!")
            return True
        self.log.append("Couldn't escape!")
        for action in self._enemy_actions():
            self._execute_action(action)
            self._check_finished()
        if self.result is None:
            self._promote_reserves()
        return False

    def resolve_capture(self, success):
        """Finish a successful wild capture or grant the opponent a free response."""
        if self.kind != BattleKind.WILD or self.result is not None:
            return self.result
        if success:
            self.result = BattleResult("captured", captured=True)
            self.log.append(f"Caught {self.enemy_pokemon.display_name}!")
            return self.result
        self.log.append(f"{self.enemy_pokemon.display_name} broke free!")
        self.enemy_response()
        return self.result

    def enemy_response(self):
        if self.result is not None:
            return self.result
        for action in self._enemy_actions():
            self._execute_action(action)
            self._check_finished()
        if self.result is None:
            self._apply_end_turn_statuses()
            self._check_finished()
        if self.result is None:
            self._promote_reserves()
        self.turn_number += 1
        return self.result

    def _opening_message(self):
        if self.kind == BattleKind.WILD:
            return f"A wild {self.enemy_team[0].species.name} appeared!"
        return f"A {self.kind.value} battle began!"

    def _valid_action(self, action):
        active = self._active_slots(action.side)
        if action.side != "player" or not 0 <= action.actor_index < len(active):
            return False
        pokemon = active[action.actor_index]
        return pokemon.current_hp > 0 and 0 <= action.move_index < len(pokemon.known_moves)

    def _enemy_actions(self):
        actions = []
        targets = self.active_team("player")
        if not targets:
            return actions
        for index, pokemon in enumerate(self._active_slots("enemy")):
            if pokemon.current_hp <= 0:
                continue
            if self.enemy_ai is not None:
                move_index, target_index = self.enemy_ai.choose(self, pokemon, targets)
                actions.append(BattleAction("enemy", index, move_index, target_index))
            else:
                usable = [i for i, move in enumerate(pokemon.known_moves) if self.remaining_pp(pokemon, move) > 0]
                if usable:
                    actions.append(BattleAction("enemy", index, self.rng.choice(usable), self.rng.randrange(len(targets))))
                else:
                    actions.append(BattleAction("enemy", index, -1, self.rng.randrange(len(targets))))
        return actions

    def _action_order(self, action):
        pokemon = self._active_slots(action.side)[action.actor_index]
        move = STRUGGLE if action.move_index == -1 else pokemon.known_moves[action.move_index]
        speed = pokemon.speed * _stage_multiplier(self.stat_stages[id(pokemon)]["speed"])
        if pokemon.status == "paralysis":
            speed *= 0.5
        return move.priority, speed, self.rng.random()

    def _execute_action(self, action):
        attackers = self._active_slots(action.side)
        defenders = self.active_team("enemy" if action.side == "player" else "player")
        if action.actor_index >= len(attackers) or not defenders:
            return
        attacker = attackers[action.actor_index]
        if attacker.current_hp <= 0:
            return
        target = defenders[min(action.target_index, len(defenders) - 1)]
        move = STRUGGLE if action.move_index == -1 else attacker.known_moves[action.move_index]
        if move is not STRUGGLE and self.remaining_pp(attacker, move) <= 0:
            if not any(self.remaining_pp(attacker, known) > 0 for known in attacker.known_moves):
                move = STRUGGLE
            else:
                self.log.append(f"{attacker.display_name} has no PP left for {move.name}!")
                return
        if move is not STRUGGLE:
            self.pp[(id(attacker), move.key)] -= 1
        if not self._can_act(attacker):
            return
        accuracy = move.accuracy * _stage_multiplier(self.stat_stages[id(attacker)]["accuracy"])
        if self.rng.uniform(0, 100) > accuracy:
            self.log.append(f"{attacker.display_name} used {move.name}, but it missed!")
            return

        attack_stat = "attack" if move.category == "physical" else "special_attack"
        defense_stat = "defense" if move.category == "physical" else "special_defense"
        damage, multiplier = calculate_damage(
            attacker, target, move, self.rng,
            self.stat_stages[id(attacker)][attack_stat], self.stat_stages[id(target)][defense_stat],
        )
        if move.effect == "hit_twice":
            damage *= 2
        target.current_hp = max(0, target.current_hp - damage)
        self.log.append(f"{attacker.display_name} used {move.name}!")
        if multiplier == 0:
            self.log.append(f"It doesn't affect {target.display_name}.")
        elif multiplier > 1:
            self.log.append("It's super effective!")
        elif multiplier < 1:
            self.log.append("It's not very effective...")
        self._apply_move_effect(attacker, target, move, damage)
        if target.current_hp == 0:
            self.log.append(f"{target.display_name} fainted!")

    def _can_act(self, pokemon):
        volatile = self.volatile[id(pokemon)]
        if volatile.pop("flinch", False):
            self.log.append(f"{pokemon.display_name} flinched!")
            return False
        if volatile.get("confusion", 0) > 0:
            volatile["confusion"] -= 1
            if self.rng.random() < (1 / 3):
                damage = max(1, pokemon.max_hp // 8)
                pokemon.current_hp = max(0, pokemon.current_hp - damage)
                self.log.append(f"{pokemon.display_name} hurt itself in confusion!")
                return False
            if volatile["confusion"] == 0:
                self.log.append(f"{pokemon.display_name} snapped out of confusion!")
        if pokemon.status == "paralysis" and self.rng.random() < 0.25:
            self.log.append(f"{pokemon.display_name} is paralyzed and cannot move!")
            return False
        if pokemon.status == "sleep":
            if self.rng.random() < 0.34:
                pokemon.status = "healthy"
                self.log.append(f"{pokemon.display_name} woke up!")
            else:
                self.log.append(f"{pokemon.display_name} is fast asleep.")
                return False
        return True

    def _apply_move_effect(self, attacker, target, move, damage):
        effect = move.effect
        if effect == "drain_half" and damage:
            attacker.current_hp = min(attacker.max_hp, attacker.current_hp + max(1, damage // 2))
        elif effect == "recoil_quarter" and damage:
            attacker.current_hp = max(0, attacker.current_hp - max(1, damage // 4))
        elif effect.startswith("lower_"):
            stat = effect.removeprefix("lower_")
            if stat in self.stat_stages[id(target)]:
                self.stat_stages[id(target)][stat] = max(-6, self.stat_stages[id(target)][stat] - 1)
                self.log.append(f"{target.display_name}'s {stat.replace('_', ' ')} fell!")
        elif effect.startswith("raise_"):
            stat = effect.removeprefix("raise_").removesuffix("_10")
            if stat in self.stat_stages[id(attacker)] and (not effect.endswith("_10") or self.rng.random() < 0.10):
                self.stat_stages[id(attacker)][stat] = min(6, self.stat_stages[id(attacker)][stat] + 1)
        elif effect == "burn_10" and target.status == "healthy" and self.rng.random() < 0.10:
            if "Fire" not in target.species.types:
                target.status = "burn"
                self.log.append(f"{target.display_name} was burned!")
        elif effect == "poison_30" and target.status == "healthy" and self.rng.random() < 0.30:
            if not {"Poison", "Steel"}.intersection(target.species.types):
                target.status = "poison"
                self.log.append(f"{target.display_name} was poisoned!")
        elif effect == "flinch_30" and self.rng.random() < 0.30:
            self.volatile[id(target)]["flinch"] = True
        elif effect == "confuse_10" and self.rng.random() < 0.10:
            self.volatile[id(target)]["confusion"] = self.rng.randint(2, 5)
            self.log.append(f"{target.display_name} became confused!")
        elif effect == "heal_next_turn":
            self.volatile[id(attacker)]["wish"] = 2
            self.log.append(f"{attacker.display_name} made a wish!")

    def _apply_end_turn_statuses(self):
        for pokemon in self.active_team("player") + self.active_team("enemy"):
            if pokemon.status in {"burn", "poison"}:
                damage = max(1, pokemon.max_hp // 8)
                pokemon.current_hp = max(0, pokemon.current_hp - damage)
                self.log.append(f"{pokemon.display_name} was hurt by {pokemon.status}!")
            volatile = self.volatile[id(pokemon)]
            if volatile.get("wish", 0) > 0:
                volatile["wish"] -= 1
                if volatile["wish"] == 0:
                    healed = min(pokemon.max_hp - pokemon.current_hp, max(1, pokemon.max_hp // 2))
                    pokemon.current_hp += healed
                    self.log.append(f"{pokemon.display_name}'s wish restored {healed} HP!")
            volatile.pop("flinch", None)

    def _check_finished(self):
        if not any(p.current_hp > 0 for p in self.enemy_team):
            xp = sum(max(1, sum(p.species.base_stats[name] for name in p.species.base_stats.__dataclass_fields__) * p.level // 35) for p in self.enemy_team)
            recipient = next((p for p in self.player_team if p.current_hp > 0), self.player_team[0])
            levels = recipient.gain_experience(xp)
            self.result = BattleResult("player", xp, levels)
            self.log.append(f"Gained {xp} experience points!")
        elif not any(p.current_hp > 0 for p in self.player_team):
            self.result = BattleResult("enemy")
            self.log.append("You are out of usable Pokémon!")

    def _promote_reserves(self):
        """Move healthy reserves into empty active slots between rounds."""
        for team in (self.player_team, self.enemy_team):
            for slot in range(min(self.active_count, len(team))):
                if team[slot].current_hp > 0:
                    continue
                replacement = next((index for index in range(self.active_count, len(team)) if team[index].current_hp > 0), None)
                if replacement is not None:
                    team[slot], team[replacement] = team[replacement], team[slot]
                    self.log.append(f"{team[slot].display_name} entered the battle!")
