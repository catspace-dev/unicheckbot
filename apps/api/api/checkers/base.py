from core.coretypes import Response
from abc import ABC


class BaseChecker(ABC):

    def __init__(self, target: str, port: int):
        self.target = target
        self.port = port

    def check(self) -> Response:
        raise NotImplementedError
