from core.coretypes import (HTTP_EMOJI, ErrorPayload, HttpCheckerResponse,
                            ResponseStatus)
from httpx import Response

from ..base import CheckerTargetPortHandler, process_args_for_host_port
from ..metrics import push_status_metric

web_help_message = """
❓ Производит проверку хоста по протоколу HTTP.

Использование:
 `/web <hostname> <port>`
 `/web <hostname>:<port>`
 `/web <hostname>` - автоматически выставит 80 порт
"""

invalid_port = """❗Неправильный порт. Напишите /web чтобы увидеть справку к данному способу проверки."""


class WebCheckerHandler(CheckerTargetPortHandler):
    help_message = web_help_message
    api_endpoint = "http"

    def __init__(self):
        super().__init__()

    def process_args(self, text: str) -> list:
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
        await push_status_metric(status, self.api_endpoint)
        return message
