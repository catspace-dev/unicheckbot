from core.coretypes import Response, ErrorPayload, ErrorCodes, ResponseStatus, ICMPCheckerResponse
from .base import BaseChecker
from icmplib import ping
from icmplib.exceptions import NameLookupError


class ICMPChecker(BaseChecker):

    def __init__(self, target: str):
        super().__init__(target)

    def create_not_alive_response(self):
        return Response(
            status=ResponseStatus.ERROR,
            payload=ErrorPayload(
                code=ErrorCodes.ICMPHostNotAlive,
                message="Host not available for ICMP ping"
            ),
            node=self.node_info
        )

    def check(self) -> Response:

        try:
            host = ping(self.target)
        except NameLookupError:
            return self.create_not_alive_response()

        # TODO: ban ping localhost
        if not host.is_alive:
            return self.create_not_alive_response()

        return Response(
            status=ResponseStatus.OK,
            payload=ICMPCheckerResponse(
                min_rtt=host.min_rtt,
                max_rtt=host.max_rtt,
                avg_rtt=host.avg_rtt,
                packets_sent=host.packets_sent,
                packets_received=host.packets_received,
                loss=host.packet_loss,
            ),
            node=self.node_info
        )
