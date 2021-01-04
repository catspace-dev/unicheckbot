from aiogram.types import Message
from tgbot.handlers.helpers import check_int
from httpx import Response
from core.coretypes import ResponseStatus, HTTP_EMOJI, HttpCheckerResponse, ErrorPayload
from ..base import CheckerBaseHandler, NotEnoughArgs, InvalidPort

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
        try:
            args = await self.process_args(message.text)
        except NotEnoughArgs:
            return await message.answer(self.help_message, parse_mode="Markdown")
        except InvalidPort:
            return await message.answer(invalid_port, parse_mode="Markdown")
        await self.check(
            message.chat.id,
            message.bot,
            dict(target=args[0], port=args[1], target_fq=f"{args[0]}:{args[1]}")
        )

    async def process_args(self, text: str) -> list:
        port = None
        args = text.split(" ")
        if len(args) < 2:
            raise NotEnoughArgs()
        if len(args) == 3:
            port = args[2]
            if not check_int(port):
                raise InvalidPort()
        if len(args) == 2:
            port = 80
        host = args[1]
        return [host, port]

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
