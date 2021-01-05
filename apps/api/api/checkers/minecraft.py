from core.coretypes import Response, PortResponse, ErrorPayload, ErrorCodes, MinecraftResponse, ResponseStatus
from mcstatus import MinecraftServer
from .base import BaseChecker
import socket


class MinecraftChecker(BaseChecker):

    def __init__(self, target: str, port: int):
        self.port = port
        super().__init__(target)

    def check(self) -> Response:
        try:
            server = MinecraftServer.lookup(f"{self.target}:{self.port}")
            status = server.status()
        except socket.gaierror:
            return Response(
                status=ResponseStatus.ERROR,
                payload=ErrorPayload(
                    message="Server does not respond!",
                    code=ErrorCodes.ConnectError
                ),
                node=self.node_info
            )
        return Response(
            status=ResponseStatus.OK,
            payload=MinecraftResponse(
                latency=status.latency,
                max_players=status.players.max,
                online=status.players.online
            ),
            node=self.node_info
        )



