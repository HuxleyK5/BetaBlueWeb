"""Versioned and size-limited multiplayer wire messages."""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import uuid


PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 64 * 1024
MESSAGE_TYPES = {"hello", "presence", "trade_offer", "trade_response", "battle_command", "battle_state", "error", "disconnect"}


class ProtocolError(ValueError):
    pass


@dataclass(frozen=True)
class MessageEnvelope:
    message_type: str
    sender_id: str
    payload: dict
    message_id: str
    sent_at: str
    protocol_version: int = PROTOCOL_VERSION

    @classmethod
    def create(cls, message_type, sender_id, payload):
        return cls(message_type, sender_id, payload, uuid.uuid4().hex, datetime.now(timezone.utc).isoformat())

    def encode(self):
        validate_envelope(self)
        try:
            encoded = json.dumps(self.to_dict(), separators=(",", ":"), sort_keys=True).encode("utf-8")
        except (TypeError, ValueError) as error:
            raise ProtocolError("Multiplayer payload is not JSON-safe") from error
        if len(encoded) > MAX_MESSAGE_BYTES:
            raise ProtocolError("Multiplayer message exceeds the size limit")
        return encoded

    def to_dict(self):
        return {"type": self.message_type, "sender_id": self.sender_id, "payload": self.payload, "message_id": self.message_id, "sent_at": self.sent_at, "protocol_version": self.protocol_version}

    @classmethod
    def decode(cls, encoded):
        if not isinstance(encoded, bytes) or len(encoded) > MAX_MESSAGE_BYTES:
            raise ProtocolError("Invalid multiplayer message bytes")
        try:
            raw = json.loads(encoded.decode("utf-8"))
            message = cls(raw["type"], raw["sender_id"], raw["payload"], raw["message_id"], raw["sent_at"], raw["protocol_version"])
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise ProtocolError("Malformed multiplayer message") from error
        validate_envelope(message)
        return message


def validate_envelope(message):
    if message.protocol_version != PROTOCOL_VERSION:
        raise ProtocolError("Unsupported multiplayer protocol version")
    if message.message_type not in MESSAGE_TYPES or not isinstance(message.payload, dict):
        raise ProtocolError("Invalid multiplayer message type or payload")
    if not all(isinstance(value, str) and value for value in (message.sender_id, message.message_id, message.sent_at)):
        raise ProtocolError("Multiplayer message identity fields are invalid")
