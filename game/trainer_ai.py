"""Move-scoring strategies for NPC trainers."""

from .type_chart import effectiveness


class TrainerAI:
    def __init__(self, difficulty="balanced", rng=None):
        self.difficulty = difficulty
        self.rng = rng

    def choose(self, battle, pokemon, targets):
        rng = self.rng or battle.rng
        usable = [(index, move) for index, move in enumerate(pokemon.known_moves) if battle.remaining_pp(pokemon, move) > 0]
        if not usable:
            return -1, rng.randrange(len(targets))
        if self.difficulty == "random":
            index, _move = rng.choice(usable)
            return index, rng.randrange(len(targets))

        scored = []
        for move_index, move in usable:
            for target_index, target in enumerate(targets):
                if move.category == "status":
                    score = 28 if target.status == "healthy" or move.effect.startswith("lower_") else 8
                else:
                    score = move.power * effectiveness(move.type_name, target.species.types)
                    if move.type_name in pokemon.species.types:
                        score *= 1.5
                    score += move.priority * 12
                scored.append((score, move_index, target_index))
        scored.sort(reverse=True)
        pool_size = 1 if self.difficulty in {"smart", "expert"} else min(2, len(scored))
        _score, move_index, target_index = rng.choice(scored[:pool_size])
        return move_index, target_index
