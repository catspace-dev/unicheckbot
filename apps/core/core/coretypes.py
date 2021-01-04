from dataclasses import dataclass
from enum import Enum, IntEnum


class Payload:
    pass


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"


class ErrorCodes(IntEnum):
    ConnectError = 1
    ICMPHostNotAlive = 2
    InvalidHostname = 3


@dataclass
class ErrorPayload(Payload):
    message: str
    code: ErrorCodes


@dataclass
class HttpCheckerResponse(Payload):
    status_code: int
    time: float


@dataclass
class ICMPCheckerResponse(Payload):
    min_rtt: float
    avg_rtt: float
    max_rtt: float
    packets_sent: int
    packets_received: int
    loss: float


@dataclass
class APINodeInfo:
    name: str
    location: str


@dataclass
class PortResponse(Payload):
    open: bool


@dataclass
class Response:
    status: ResponseStatus
    payload: Payload
    node: APINodeInfo


@dataclass
class APINode:
    address: str
    token: str


HTTP_EMOJI = {
    2: "✅",
    3: "➡️",
    4: "🔍",
    5: "❌️",
}
