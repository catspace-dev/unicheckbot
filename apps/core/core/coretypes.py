from dataclasses import dataclass
from enum import Enum, IntEnum


class Payload:
    pass


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"


class HttpErrorCodes(IntEnum):
    ConnectError = 1


@dataclass
class ErrorPayload(Payload):
    message: str
    code: HttpErrorCodes


@dataclass
class HttpCheckerResponse(Payload):
    status_code: int
    time: float


@dataclass
class Response:
    status: ResponseStatus
    payload: Payload


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
