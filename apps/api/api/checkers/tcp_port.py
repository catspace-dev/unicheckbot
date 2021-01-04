from core.coretypes import Response, PortResponse, ResponseStatus, ErrorPayload, ErrorCodes
from .base import BaseChecker
import socket


class TCPPortChecker(BaseChecker):

    def __init__(self, target: str, port: int):
        self.port = port
        super().__init__(target)

    def check(self) -> Response:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2 seconds timeout...
        sock.settimeout(2)

        try:
            res = sock.connect_ex((self.target, self.port))
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
            sock.close()
            return Response(
                status=ResponseStatus.OK,
                payload=PortResponse(open=True),
                node=self.node_info
            )
        sock.close()
        return Response(
            status=ResponseStatus.OK,
            payload=PortResponse(open=False),
            node=self.node_info
        )


