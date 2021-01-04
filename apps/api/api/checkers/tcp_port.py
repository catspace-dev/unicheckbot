from core.coretypes import Response
from .base import BaseChecker


class TCPPortChecker(BaseChecker):

    def __init__(self, target: str):
        super().__init__(target)

    def check(self) -> Response:
        pass
