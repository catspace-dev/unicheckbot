from aiogram.types import Message
from core.coretypes import ResponseStatus, ErrorPayload, PortResponse
from httpx import Response

from tgbot.handlers.base import CheckerTargetPortHandler, NotEnoughArgs, InvalidPort
from tgbot.handlers.helpers import check_int
from tgbot.handlers.metrics import push_status_metric
from tgbot.middlewares.throttling import rate_limit

tcp_help_message = """
❓ Производит проверку TCP порта, открыт ли он или нет

Использование:
 `/tcp <hostname> <port>` 
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

    async def process_args(self, text: str) -> list:
        args = text.split(' ', 1)
        if len(args) != 2:
            raise NotEnoughArgs()
        host = args[1]
        if ":" in host:
            host, port = host.rsplit(":", 1)
        elif " " in host:
            host, port = host.split(maxsplit=1)
        else:
            raise NotEnoughArgs()
        if not check_int(port):
            raise InvalidPort()
        return [host, port]

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
