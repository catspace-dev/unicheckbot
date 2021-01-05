from aiogram.types import Message
from core.coretypes import ResponseStatus, ErrorPayload, PortResponse
from httpx import Response

from tgbot.handlers.base import CheckerBaseHandler, NotEnoughArgs, InvalidPort
from tgbot.handlers.helpers import check_int

tcp_help_message = """
❓ Производит проверку TCP порта, открыт ли он или нет

Использование:
 `/tcp <hostname> <port>` 
"""

invalid_port = """❗Неправильный порт. Напишите /tcp чтобы увидеть справку к данному способу проверки."""


class TCPCheckerHandler(CheckerBaseHandler):
    help_message = tcp_help_message
    api_endpoint = "tcp_port"

    def __init__(self):
        super().__init__()

    async def handler(self, message: Message):
        await self.target_port_handler(message)

    async def process_args(self, text: str) -> list:
        port = None
        args = text.split(" ")
        if len(args) < 3:
            raise NotEnoughArgs()
        if len(args) >= 3:
            port = args[2]
            if not check_int(port):
                raise InvalidPort()
        host = args[1]
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
        return message
