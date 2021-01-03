from core.coretypes import (
    Response, HttpCheckerResponse, APINodeInfo,
    ResponseStatus, ErrorCodes, ErrorPayload,
)
from requests import Session
from requests.exceptions import ConnectionError
from .base import BaseChecker
from api.config import NODE_NAME, NODE_LOCATION
import time
import re


class HttpChecker(BaseChecker):

    default_schema = "http://"
    default_schema_re = re.compile("^[hH][tT][tT][pP].*")

    def __init__(self, target: str, port: int):
        super(HttpChecker, self).__init__(target)
        self.port = port
        self.session = Session()

    def check(self) -> Response:

        url = f"{self.target}:{self.port}"
        if not self.default_schema_re.match(url):
            url = f"{self.default_schema}{url}"

        start_time = time.time()
        try:
            request = self.session.get(
                url
            )
        # TODO: requests.exceptions.InvalidURL failed to parse exception
        except ConnectionError:
            return Response(
                status=ResponseStatus.ERROR,
                payload=ErrorPayload(
                    message="Failed to establish a new connection",
                    code=ErrorCodes.ConnectError,
                ),
                node=self.node_info
            )

        end_time = time.time()

        return Response(
            status=ResponseStatus.OK,
            payload=HttpCheckerResponse(
                time=end_time - start_time,
                status_code=request.status_code
            ),
            node=self.node_info
        )
