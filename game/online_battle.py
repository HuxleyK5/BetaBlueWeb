"""Deterministic command contract for future authoritative online battles."""

from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class OnlineBattleCommand:
    match_id: str
    player_id: str
    turn: int
    actor_index: int
    move_index: int
    target_index: int = 0

    def to_dict(self):
        return self.__dict__.copy()


@dataclass(frozen=True)
class MatchSnapshot:
    match_id: str
    player_ids: tuple[str, str]
    seed: int
    turn: int
    teams: dict


class OnlineBattleCoordinator:
    """Validates command order; a future server will own this same contract."""

    def create_match(self, player_a, team_a, player_b, team_b, seed):
        if player_a.player_id == player_b.player_id:
            raise ValueError("An online match requires two players")
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise ValueError("Match seed must be an integer")
        if not 1 <= len(team_a) <= 6 or not 1 <= len(team_b) <= 6:
            raise ValueError("Online teams require one to six Pokemon")
        identifiers = [pokemon.pokemon_id for pokemon in list(team_a) + list(team_b)]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Online teams contain duplicate Pokemon identities")
        return MatchSnapshot(uuid.uuid4().hex, (player_a.player_id, player_b.player_id), seed, 1, {player_a.player_id: [p.to_dict() for p in team_a], player_b.player_id: [p.to_dict() for p in team_b]})

    @staticmethod
    def validate_command(match, command):
        return (
            command.match_id == match.match_id and command.player_id in match.player_ids
            and command.turn == match.turn and command.actor_index >= 0
            and command.move_index >= 0 and command.target_index >= 0
        )
