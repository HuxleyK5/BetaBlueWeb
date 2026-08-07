"""Multiplayer foundation abstractions and placeholders."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MultiplayerSession:
    session_id: str
    connected_players: int = 1
    match_state: Optional[str] = None


class MultiplayerManager:
    def __init__(self):
        self.active_session: Optional[MultiplayerSession] = None

    def host_session(self, session_id: str):
        self.active_session = MultiplayerSession(session_id=session_id, connected_players=1)
        return self.active_session

    def join_session(self, session_id: str):
        if self.active_session and self.active_session.session_id == session_id:
            self.active_session.connected_players += 1
            return self.active_session
        return None

    def leave_session(self):
        if self.active_session:
            self.active_session.connected_players = max(0, self.active_session.connected_players - 1)
            if self.active_session.connected_players == 0:
                self.active_session = None
