from core.coretypes import Response, APINodeInfo
from api.config import NODE_NAME, NODE_LOCATION
from abc import ABC


class BaseChecker(ABC):

    def __init__(self, target: str):
        self.target = target
        self.node_info = APINodeInfo(
            name=NODE_NAME, location=NODE_LOCATION
        )

    def check(self) -> Response:
        raise NotImplementedError
