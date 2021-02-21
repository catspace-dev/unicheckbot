from typing import Tuple

from aiogram.types import Message
from core.coretypes import ErrorPayload, PortResponse, ResponseStatus
from httpx import Response

from ...middlewares.throttling import rate_limit
from ..base import (CheckerTargetPortHandler, InvalidPort, NotEnoughArgs,
                    parse_host_port)
from ..metrics import push_status_metric

tcp_help_message = """
❓ Производит проверку TCP порта, открыт ли он или нет

Использование:
 `/tcp <hostname> <port>`
 `/tcp <hostname>:<port>`
"""

invalid_port = """❗Неправильный порт. Напишите /tcp чтобы увидеть справку к данному способу проверки."""


class TCPCheckerHandler(CheckerTargetPortHandler):
    help_message = tcp_help_message
    api_endpoint = "tcp_port"

    def __init__(self):
        super().__init__()

    @rate_limit
    async def handler(self, message: Message):
        await super(TCPCheckerHandler, self).handler(message)

    def process_args(self, text: str) -> Tuple[str, int]:
        args = text.split(' ', 1)
        if len(args) != 2:
            raise NotEnoughArgs()
        host = args[1]
        host, port = parse_host_port(host, -1)
        if port == -1:
            raise NotEnoughArgs()
        return (host, port)

    async def prepare_message(self, res: Response):
        message, status = await self.message_std_vals(res)
        if status == ResponseStatus.OK:
            payload = PortResponse(**res.json().get("payload"))
            if payload.open:
                message += "✅ Порт ОТКРЫТ"
            else:
                message += "❌️ Порт ЗАКРЫТ"
        if status == ResponseStatus.ERROR:
            payload = ErrorPayload(**res.json().get("payload"))
            message += f"❌️ {payload.message}"
        await push_status_metric(status, self.api_endpoint)
        return message
