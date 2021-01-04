from core.coretypes import Response, PortResponse, ResponseStatus, ErrorPayload, ErrorCodes
from .base import BaseChecker
import socket


class PortChecker(BaseChecker):

    def __init__(self, target: str, port: int, sock: socket.socket):
        self.port = port
        self.sock = sock
        super().__init__(target)

    def check(self) -> Response:
        # 2 seconds timeout...
        self.sock.settimeout(2)

        try:
            res = self.sock.connect_ex((self.target, self.port))
        except socket.gaierror:
            return Response(
                status=ResponseStatus.ERROR,
                payload=ErrorPayload(
                    message="Invalid hostname",
                    code=ErrorCodes.InvalidHostname
                ),
                node=self.node_info
            )
        if res == 0:
            self.sock.close()
            return Response(
                status=ResponseStatus.OK,
                payload=PortResponse(open=True),
                node=self.node_info
            )
        self.sock.close()
        return Response(
            status=ResponseStatus.OK,
            payload=PortResponse(open=False),
            node=self.node_info
        )


