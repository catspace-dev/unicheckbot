from core.coretypes import (
    Response, HttpCheckerResponse,
    ResponseStatus, HttpErrorCodes, ErrorPayload
)
from requests import Session
from requests.exceptions import ConnectionError
from .base import BaseChecker
import time
import re


class HttpChecker(BaseChecker):

    default_schema = "http://"
    default_schema_re = re.compile("^[hH][tT][tT][pP].*")

    def __init__(self, target: str, port: int):
        super(HttpChecker, self).__init__(target, port)
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
        except ConnectionError:
            return Response(
                status=ResponseStatus.ERROR,
                payload=ErrorPayload(
                    message="Failed to establish a new connection",
                    code=HttpErrorCodes.ConnectError
                )
            )

        end_time = time.time()

        return Response(
            status=ResponseStatus.OK,
            payload=HttpCheckerResponse(
                time=end_time - start_time,
                status_code=request.status_code
            )
        )
