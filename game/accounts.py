"""Player identity boundary with an offline provider by default."""

from dataclasses import dataclass
from typing import Protocol
import uuid


@dataclass(frozen=True)
class PlayerIdentity:
    player_id: str
    display_name: str
    provider: str = "offline"
    authenticated: bool = False

    def to_dict(self):
        return {"player_id": self.player_id, "display_name": self.display_name, "provider": self.provider, "authenticated": self.authenticated}


class AccountProvider(Protocol):
    def create_guest(self, display_name: str) -> PlayerIdentity: ...
    def sign_in(self, credentials: dict) -> PlayerIdentity: ...
    def sign_out(self) -> None: ...


class OfflineAccountProvider:
    """Local identity implementation; never performs network or credential I/O."""

    def __init__(self):
        self.identity = None

    def create_guest(self, display_name="Trainer"):
        self.identity = PlayerIdentity(uuid.uuid4().hex, display_name or "Trainer")
        return self.identity

    def restore(self, data):
        try:
            identity = PlayerIdentity(data["player_id"], data["display_name"], data.get("provider", "offline"), bool(data.get("authenticated", False)))
        except (KeyError, TypeError) as error:
            raise ValueError("invalid saved player identity") from error
        if not identity.player_id or not identity.display_name:
            raise ValueError("invalid saved player identity")
        self.identity = identity
        return identity

    def rename_guest(self, display_name):
        if self.identity is None:
            return self.create_guest(display_name)
        self.identity = PlayerIdentity(self.identity.player_id, display_name, self.identity.provider, self.identity.authenticated)
        return self.identity

    def sign_in(self, credentials):
        raise RuntimeError("No online account provider is configured.")

    def sign_out(self):
        self.identity = None
