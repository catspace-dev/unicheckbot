from .port import PortChecker
import socket


class TCPPortChecker(PortChecker):

    def __init__(self, target: str, port: int):
        super().__init__(
            target=target,
            port=port,
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        )

