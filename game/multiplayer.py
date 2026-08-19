"""Transport-neutral multiplayer sessions with an offline loopback default."""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .network_protocol import MessageEnvelope


class ConnectionState(str, Enum):
    OFFLINE = "offline"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class Transport(Protocol):
    def connect(self) -> None: ...
    def send(self, payload: bytes) -> None: ...
    def poll(self) -> list[bytes]: ...
    def close(self) -> None: ...


class LoopbackTransport:
    """Deterministic test transport; it never opens a socket."""

    def __init__(self):
        self.connected = False
        self.queue = []

    def connect(self): self.connected = True
    def send(self, payload):
        if not self.connected:
            raise ConnectionError("Loopback transport is offline")
        self.queue.append(payload)
    def poll(self):
        messages, self.queue = self.queue, []
        return messages
    def close(self): self.connected = False; self.queue.clear()


@dataclass
class MultiplayerSession:
    identity: object
    state: ConnectionState = ConnectionState.OFFLINE
    last_error: str = ""


class MultiplayerGateway:
    def __init__(self, identity, transport=None):
        self.session = MultiplayerSession(identity)
        self.transport = transport or LoopbackTransport()

    def connect_loopback(self):
        self.session.state = ConnectionState.CONNECTING
        try:
            self.transport.connect()
            self.session.state = ConnectionState.CONNECTED
            self.send("hello", {"display_name": self.session.identity.display_name})
        except Exception as error:
            self.session.state, self.session.last_error = ConnectionState.ERROR, str(error)
        return self.session.state

    def send(self, message_type, payload):
        envelope = MessageEnvelope.create(message_type, self.session.identity.player_id, payload)
        self.transport.send(envelope.encode())
        return envelope

    def poll(self):
        return [MessageEnvelope.decode(payload) for payload in self.transport.poll()]

    def disconnect(self):
        self.transport.close()
        self.session.state = ConnectionState.OFFLINE
