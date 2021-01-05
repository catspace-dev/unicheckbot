from aiogram.types import Message
from httpx import Response
from core.coretypes import ResponseStatus, HTTP_EMOJI, HttpCheckerResponse, ErrorPayload
from ..base import CheckerBaseHandler, NotEnoughArgs, InvalidPort, process_args_for_host_port

web_help_message = """
❓ Производит проверку хоста по протоколу HTTP.

Использование:
 `/web <hostname> <port>` 
 `/web <hostname>` - автоматически выставит 80 порт
"""

invalid_port = """❗Неправильный порт. Напишите /web чтобы увидеть справку к данному способу проверки."""


class WebCheckerHandler(CheckerBaseHandler):
    help_message = web_help_message
    api_endpoint = "http"

    def __init__(self):
        super().__init__()

    async def handler(self, message: Message):
        await self.target_port_handler(message)

    async def process_args(self, text: str) -> list:
        return process_args_for_host_port(text, 80)

    async def prepare_message(self, res: Response):
        message, status = await self.message_std_vals(res)
        if status == ResponseStatus.OK:
            payload = HttpCheckerResponse(**res.json().get("payload"))
            message += f"{HTTP_EMOJI.get(payload.status_code // 100, '')} " \
                       f"{payload.status_code}, ⏰ {payload.time * 1000:.2f}ms"
        if status == ResponseStatus.ERROR:
            payload = ErrorPayload(**res.json().get("payload"))
            message += f"❌️ {payload.message}"
        return message
